from models.database import get_session
from models.entities import Categoria, UnidadMedida, Usuario, Rol, Producto

def obtener_categorias():
    session = get_session()
    if not session: return []
    try:
        categorias = session.query(Categoria).all()
        return [{"id": c.ID_CATEGORIA, "nombre": c.NOMBRE_CATEGORIA} for c in categorias]
    except Exception:
        return []
    finally:
        session.close()

def obtener_unidades():
    session = get_session()
    if not session: return []
    try:
        unidades = session.query(UnidadMedida).all()
        return [{"id": u.ID_UNIDAD, "nombre": f"{u.NOMBRE_UNIDAD} ({u.SIMBOLO})"} for u in unidades]
    except Exception:
        return []
    finally:
        session.close()

def obtener_roles():
    session = get_session()
    if not session: return []
    try:
        roles = session.query(Rol).all()
        return [{"id": r.ID_ROL, "nombre": r.NOMBRE_ROL} for r in roles]
    except Exception:
        return []
    finally:
        session.close()

def obtener_usuarios():
    session = get_session()
    if not session: return []
    try:
        usuarios = session.query(Usuario).join(Rol).all()
        return [{"id": u.ID_USUARIO, "nombre": u.NOMBRE_COMPLETO, "correo": u.CORREO, "id_rol": u.ID_ROL, "rol": u.rol.NOMBRE_ROL, "estado": u.ESTADO} for u in usuarios]
    except Exception:
        return []
    finally:
        session.close()

def crear_usuario(nombre, correo, password, id_rol):
    session = get_session()
    if not session: return False
    try:
        nuevo = Usuario(NOMBRE_COMPLETO=nombre, CORREO=correo, PASSW_ORD=password, ID_ROL=id_rol, ESTADO=True)
        session.add(nuevo)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def actualizar_usuario(id_usr, nombre, correo, password, id_rol):
    session = get_session()
    if not session: return False
    try:
        u = session.query(Usuario).get(id_usr)
        if u:
            u.NOMBRE_COMPLETO = nombre
            u.CORREO = correo
            if password: # Si está vacío, no cambia la contraseña
                u.PASSW_ORD = password
            u.ID_ROL = id_rol
            session.commit()
            return True
        return False
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()

def toggle_estado_usuario(id_usuario):
    session = get_session()
    if not session: return
    try:
        u = session.query(Usuario).get(id_usuario)
        if u:
            u.ESTADO = not u.ESTADO
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

def obtener_catalogo():
    session = get_session()
    if not session: return []
    try:
        productos = session.query(Producto).all()
        return [{"id": p.ID_PRODUCTO, "codigo": p.CODIGO_UNICO, "desc": p.DESCRIPCION_PRODUCTO, 
                 "id_cat": p.ID_CATEGORIA, "id_uni": p.ID_UNIDAD, 
                 "stock_min": p.STOCK_MINIMO, "costo": p.COSTO_PROMEDIO, "estado": p.ESTADO} for p in productos]
    except Exception:
        return []
    finally:
        session.close()

def crear_producto(codigo, desc, id_categoria, id_unidad, stock_min, costo):
    session = get_session()
    if not session: return False
    try:
        nuevo = Producto(CODIGO_UNICO=codigo, DESCRIPCION_PRODUCTO=desc, ID_CATEGORIA=id_categoria, ID_UNIDAD=id_unidad, STOCK_MINIMO=stock_min, COSTO_PROMEDIO=costo, ESTADO=True)
        session.add(nuevo)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def actualizar_producto(id_prod, codigo, desc, id_categoria, id_unidad, stock_min, costo):
    session = get_session()
    if not session: return False
    try:
        p = session.query(Producto).get(id_prod)
        if p:
            p.CODIGO_UNICO = codigo
            p.DESCRIPCION_PRODUCTO = desc
            p.ID_CATEGORIA = id_categoria
            p.ID_UNIDAD = id_unidad
            p.STOCK_MINIMO = stock_min
            p.COSTO_PROMEDIO = costo
            session.commit()
            return True
        return False
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()

def toggle_estado_producto(id_producto):
    session = get_session()
    if not session: return
    try:
        p = session.query(Producto).get(id_producto)
        if p:
            p.ESTADO = not p.ESTADO
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

def obtener_ajustes_pendientes():
    """Consulta movimientos que están en estado EN REVISION."""
    session = get_session()
    if not session: return []
    try:
        from models.entities import MovimientoKardex
        movs = session.query(MovimientoKardex)\
            .filter(MovimientoKardex.ESTADO_APROBACION == 'EN REVISION')\
            .order_by(MovimientoKardex.FECHA_MOVIMIENTO.asc()).all()
            
        resultado = []
        for m in movs:
            for det in m.detalles:
                resultado.append({
                    "id_movimiento": m.ID_MOVIMIENTO,
                    "folio": m.FOLIO_COMPROBANTE,
                    "fecha": m.FECHA_MOVIMIENTO.strftime("%d/%m/%Y %I:%M %p"),
                    "tipo": m.tipo_movimiento.NOMBRE_TIPO if m.tipo_movimiento else "AJUSTE",
                    "solicitante": m.usuario_registro.NOMBRE_COMPLETO if m.usuario_registro else "-",
                    "bodega": (m.bodega_destino.NOMBRE_BODEGA if m.bodega_destino else (m.bodega_origen.NOMBRE_BODEGA if m.bodega_origen else "-")),
                    "id_bodega": m.ID_BODEGA_DESTINO or m.ID_BODEGA_ORIGEN,
                    "id_producto": det.ID_PRODUCTO,
                    "producto": det.producto.DESCRIPCION_PRODUCTO if det.producto else "-",
                    "codigo": det.producto.CODIGO_UNICO if det.producto else "-",
                    "cantidad": float(det.CANTIDAD or 0),
                    "costo": float(det.COSTO_UNITARIO or 0),
                    "motivo": m.motivo.DESCRIPCION_MOTIVO if m.motivo else "Ajuste de inventario",
                    "observaciones": m.OBSERVACIONES or "-",
                    "efecto": m.tipo_movimiento.EFECTO_STOCK if m.tipo_movimiento else 1
                })
        return resultado
    except Exception:
        return []
    finally:
        session.close()

def aprobar_ajuste(id_movimiento, id_usuario_admin):
    """Aprueba un ajuste de inventario y aplica el cambio al stock físico de forma transaccional."""
    from datetime import datetime
    session = get_session()
    if not session:
        return False, "Base de datos no disponible."
    try:
        from models.entities import MovimientoKardex, ExistenciaBodega
        mov = session.query(MovimientoKardex).get(id_movimiento)
        if not mov or mov.ESTADO_APROBACION != 'EN REVISION':
            return False, "El movimiento no existe o ya fue procesado."
            
        efecto = mov.tipo_movimiento.EFECTO_STOCK if mov.tipo_movimiento else 1
        bodega_id = mov.ID_BODEGA_DESTINO if efecto > 0 else (mov.ID_BODEGA_ORIGEN or mov.ID_BODEGA_DESTINO)
        
        for det in mov.detalles:
            existencia = session.query(ExistenciaBodega).filter_by(
                ID_PRODUCTO=det.ID_PRODUCTO, ID_BODEGA=bodega_id
            ).first()
            
            saldo_anterior = float(existencia.STOCK_ACTUAL if existencia else 0.0)
            saldo_nuevo = saldo_anterior + (float(det.CANTIDAD) * efecto)
            
            if efecto < 0 and saldo_nuevo < 0:
                raise ValueError(f"Stock insuficiente en bodega para aprobar el ajuste negativo. Disponible: {saldo_anterior}")
                
            if existencia:
                existencia.STOCK_ACTUAL = saldo_nuevo
            else:
                nueva_existencia = ExistenciaBodega(ID_PRODUCTO=det.ID_PRODUCTO, ID_BODEGA=bodega_id, STOCK_ACTUAL=saldo_nuevo)
                session.add(nueva_existencia)
                
            det.SALDO_ANTERIOR = saldo_anterior
            det.SALDO_NUEVO = saldo_nuevo
            
        mov.ESTADO_APROBACION = 'APROBADO'
        mov.ID_USUARIO_AUTORIZA = id_usuario_admin
        mov.FECHA_AUTORIZACION = datetime.now()
        
        session.commit()
        return True, "Ajuste aprobado y aplicado al inventario exitosamente."
    except ValueError as ve:
        session.rollback()
        return False, str(ve)
    except Exception as e:
        session.rollback()
        return False, f"Error al aprobar ajuste: {str(e)}"
    finally:
        session.close()

def rechazar_ajuste(id_movimiento, id_usuario_admin, motivo_rechazo=""):
    """Rechaza un ajuste de inventario sin alterar el stock."""
    from datetime import datetime
    session = get_session()
    if not session:
        return False, "Base de datos no disponible."
    try:
        from models.entities import MovimientoKardex
        mov = session.query(MovimientoKardex).get(id_movimiento)
        if not mov or mov.ESTADO_APROBACION != 'EN REVISION':
            return False, "El movimiento no existe o ya fue procesado."
            
        mov.ESTADO_APROBACION = 'RECHAZADO'
        mov.ID_USUARIO_AUTORIZA = id_usuario_admin
        mov.FECHA_AUTORIZACION = datetime.now()
        if motivo_rechazo:
            mov.OBSERVACIONES = (mov.OBSERVACIONES or "") + f" [Rechazado por Admin: {motivo_rechazo}]"
            
        session.commit()
        return True, "Solicitud de ajuste rechazada."
    except Exception as e:
        session.rollback()
        return False, f"Error al rechazar ajuste: {str(e)}"
    finally:
        session.close()

