"""
decorated_stem.py - Decorated Stem
"""
from flatland.database.flatlanddb import FlatlandDB as fdb
from sqlalchemy import select, and_


class DecoratedStem:
    """
    A Stem Signification that is decorated somehow when it appears on a Diagram is considered a
    Decorated Stem. Not all Stem Significations are decorated. The stem attaching a class diagram
    subclass is not notated in many class diagram notations.
    """
    def __init__(self, stem_type: 'str', semantic: 'str', notation: 'str', diagram_type_name: 'str'):
        """
        Constructor

        :param stem_type:
        :param semantic:
        :param notation:
        :param diagram_type_name:
        """
        self.Stem_type = stem_type
        self.Root_symbol = None
        self.Vine_symbol = None
        self.Label = None

        stem_end_dec_t = fdb.MetaData.tables['Stem End Decoration']
        p = [stem_end_dec_t.c.Symbol, stem_end_dec_t.c.End]
        r = and_(
            (stem_end_dec_t.c['Stem type'] == self.Stem_type),
            (stem_end_dec_t.c['Diagram type'] == diagram_type_name),
            (stem_end_dec_t.c.Notation == notation),
            (stem_end_dec_t.c.Semantic == semantic)
        )
        q = select(p).where(r)
        rows = fdb.Connection.execute(q).fetchall()
        for r in rows:
            if r.End == 'root':
                self.Root_symbol = r.Symbol
            elif r.End == 'vine':
                self.Vine_symbol = r.Symbol
            else:  # Illegal enum value in database for some reason
                assert False, f"Illegal enum value for End in {stem_type}"

        # TODO: Lookup Label also


