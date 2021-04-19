#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl = pkg.table('deposito', pkey='id', name_long='!![it]Deposito', name_plural='!![it]Deposito', 
                                caption_field='nome', lookup=True)
        self.sysFields(tbl)
        
        tbl.column('codice', size='3', name_long='!![it]Codice', unmodifiable=True)
        tbl.column('nome', size=':50', name_long='!![it]Nome')
        tbl.column('anagrafica_id',size='22', group='_', name_long='Anagrafica'
                    ).relation('erpy_base.anagrafica.id', relation_name='deposito', mode='foreignkey', onDelete='raise')

    def trigger_onInserting(self, record):
        if len(record['codice'])>3 or not record['codice'].isupper():
            print(len(record['codice']), record['codice'].isupper())
            record['codice'] = record['nome'][:3].upper()

    def partitionioning_pkeys(self):
        sezione_id = self.db.currentEnv.get('current_sezione_id')
        if sezione_id:
            return [r['pkey'] for r in self.query(where='$sezione_id=:sez_id', sez_id=sezione_id).fetch()]
        else:
            return [r['pkey'] for r in self.query().fetch()]