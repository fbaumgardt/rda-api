import time, sys

from flask import current_app as app
from flask import json, request
from flask.views import MethodView

from src.utils.base.errors import *
from src.utils.data.cursor import cursor
from .models import *

profile = False

class MemberView(MethodView):

    def flatten(self, ls):
        return [m for l in ls for m in l]

    def recurse(self, m_obj, depth):
        if depth is 0:
            return m_obj
        else:
            try:
                m_objs = app.db.get_member(m_obj.id)
                return MemberResultSet([self.recurse(m, depth-1) for m in m_objs])
            except:
                return m_obj

    def getParams(self, args):
        datatype = request.args.get("f_datatype")
        role = request.args.get("f_role")
        index = request.args.get("f_index")
        date_added = request.args.get("f_dateAdded")
        expand_depth = int(request.args.get("expandDepth") or 0)
        cursor_string = request.args.get("cursor")
        return [datatype, role, index, date_added, expand_depth, cursor_string]

    def get(self, id, mid=None):
        try:
            if mid:
                #if profile:
                #    start = time.time()
                members = app.db.get_member(id, mid)
                #if profile:
                #    print("GET MEMBER: ",time.time()-start)
                result = members[0]
            else:
                next = None
                prev = None
                datatype, role, index, date_added, expand_depth, cursor_string = self.getParams(request.args)
                filter = [f for f in [
                    {'type': MemberItem, 'path':['datatype'], 'value':datatype},
                    {'type': MemberItem, 'path':['mappings', 'role'], 'value':role},
                    {'type': MemberItem, 'path':['mappings', 'index'], 'value':index},
                    {'type': MemberItem, 'path':['mappings', 'dateAdded'], 'value':date_added}
                ] if f.get('value') is not None]
                collection = app.db.get_collection(id).pop()
                members = app.db.get_member(id,filter=filter)
                if expand_depth is not 0:
                    members = [self.recurse(m, expand_depth) for m in members]
                if collection.capabilities.isOrdered:
                    members = sorted(members, key=lambda m: m.mappings.index if hasattr(m, "mappings") and hasattr(m.mappings, "index") else sys.maxsize)
                if cursor_string:
                    crsr = cursor.fromString(cursor_string)
                    if len(members)>crsr.end:
                        next = crsr.next()
                    if crsr.start:
                        prev = crsr.prev()
                    members = members[crsr.start:crsr.end]
                result = MemberResultSet(members, prevCursor=(request.url.replace("cursor="+cursor_string,"cursor="+prev.toString()) if prev else None), nextCursor=(request.url.replace("cursor="+cursor_string,"cursor="+next.toString()) if next else None))
            return jsonify(result), 200
        except (NotFoundError, DBError, UnauthorizedError):
            raise
        except:
            raise ParseError()

    def post(self, id):
        try:
            if not id:
                raise NotFoundError()
            obj = json.loads(request.data)
            if not isinstance(obj, list):
                obj=[obj]
            # todo: raise parseError if
            #if not isinstance(obj, Model):
            #    if app.db.get_service().providesCollectionPids:
            #        obj += {'id': app.db.get_id(MemberItem)}
            #        obj = MemberItem(**obj)
            #if profile:
            #    start = time.time()
            # todo: check if ids are currently in use


            res = app.db.ask_member(id, [o.id for o in obj])
            if res>0:
                raise ConflictError()
            #if profile:
            #    print("CHECK EXISTING MEMBER:  ",time.time()-start)
            #    start = time.time()
            # todo change db interface to create/update? where create fails if item exists and update fails if it doesnt
            app.db.set_member(id, obj)
            #if profile:
            #    print("WRITE MEMBER: ",time.time()-start)


            return jsonify(app.db.get_member(id, [o.id for o in obj])), 201
        except (NotFoundError, DBError, UnauthorizedError, ForbiddenError, ConflictError):
            raise
        except:
            raise ParseError()

    def put(self, id, mid):
        try:
            posted = json.loads(request.data)
            if posted.id != mid:
                raise ParseError()
            if len(app.db.get_member(id, mid)) is not 1:
                raise NotFoundError()
            app.db.set_member(id, posted)
            return jsonify(MemberResultSet([posted])), 200
        except (NotFoundError, DBError, UnauthorizedError):
            raise
        except:
            raise ParseError()

    def delete(self, id, mid):
        try:
            app.db.del_member(id, mid)
            return jsonify(), 200  # todo: use id, mid
        except (NotFoundError, DBError, UnauthorizedError):
            raise
        except:
            raise ParseError()


class PropertiesView(MethodView):

    def write(self, cur, keys, value, create=False):
        if len(keys) == 1:
            cur[keys[0]] = value
            return
        if create and not cur.has_key(keys[0]):
            cur[keys[0]] = {}
        self.write(cur[keys[0]], keys[1:], value)

    def get(self, id, mid, property):
        try:
            result = app.db.get_member(id,mid).dict()
            for key in property.split('.'):
                result = result[key]
            return jsonify(result), 200
        except (NotFoundError, DBError, UnauthorizedError):
            raise
        except:
            raise ParseError()

    def put(self, id, mid, property):
        try:
            posted = json.loads(request.data)['content']
            m_dict = app.db.get_member(id,mid).dict()
            self.write(m_dict, property.split("."), posted)
            if m_dict.get('mappings') and not isinstance(m_dict['mappings'], Model):
                m_dict['mappings'] = CollectionItemMappingMetadata(**m_dict['mappings'])
            return jsonify(app.db.set_member(MemberItem(**m_dict))), 200
        except (NotFoundError, DBError, UnauthorizedError):
            raise
        except:
            raise ParseError()

    def delete(self, id, mid, property):
        try:
            return jsonify(), 200  # todo: use id, mid, property
        except (NotFoundError, DBError, UnauthorizedError):
            raise
        except:
            raise ParseError()


members = {
    'members': MemberView.as_view('members'),
    'properties': PropertiesView.as_view('properties'),
}