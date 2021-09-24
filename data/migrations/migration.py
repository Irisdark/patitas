

rol1 = Rol(tipo_rol='Administrador')
db.session.add(rol1)
db.session.commit()

rol2 = Rol(tipo_rol='Común')
db.session.add(rol2)
db.session.commit()

rol3 = Rol(tipo_rol='Desactivado')
db.session.add(rol3)
db.session.commit()


