print("INICIANDO INSERCION")

period_model = env['tcu.period']

print("MODELO OK")

period_model.create({
    'name': 'TCU I 2026',
    'year': '2026',
    'start_date': '2026-01-15',
    'end_date': '2026-06-30',
    'active': True
})

print("PERIODO 1 INSERTADO")

period_model.create({
    'name': 'TCU II 2026',
    'year': '2026',
    'start_date': '2026-07-01',
    'end_date': '2026-12-15',
    'active': True
})
env.cr.commit()
print("PERIODO 2 INSERTADO")