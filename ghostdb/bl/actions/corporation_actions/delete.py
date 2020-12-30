import typing

from ghostdb.db.models import corporation
from sqlalchemy_utils.primitives import Ltree
from ..utils import base


class Delete(base.BaseAction):

    def process(self, corp: corporation.Corporation) -> typing.Tuple[corporation.Corporation, bool]:
        self.db.delete(corp)
        self.db.commit()

        return (corp, True)


class DeleteMember(base.BaseAction):

    def process(self, member: corporation.Member) -> typing.Tuple[corporation.Member, bool]:

        # if member.path is None that it's a root
        # else we must rebuild path for subordinates
        if member.path:
            sql = '''
                UPDATE "{table_name}"
                SET
                  "{column_name}" = (:parent_path)::ltree ||
                  CASE WHEN nlevel("{table_name}"."{column_name}") = nlevel(:member_path) THEN ''
                  ELSE subpath("{table_name}"."{column_name}", nlevel(:member_path))
                  END
                WHERE
                 "{column_name}" <@ :member_path
            '''

            self.db.execute(
                sql.format(
                    table_name=corporation.Member.__tablename__,
                    column_name=corporation.Member.path._query_clause_element().name,
                ),
                {
                    'member_path': (member.path + Ltree(member.id.hex)).path,
                    'parent_path': member.path.path
                }
            )

        self.db.delete(member)

        return (member, True)
