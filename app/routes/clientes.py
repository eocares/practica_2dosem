from datetime import date
from flask import Blueprint, Response, jsonify, redirect, render_template, request, url_for
from ..services import cliente_service as svc

bp = Blueprint("clientes", __name__)


def _datos():
    return request.get_json(silent=True) or request.form


@bp.route("/")
def inicio():
    return render_template("clientes/form.html", cliente=None, intereses=svc.intereses_activos(),
                           action=url_for("clientes.registro"), redirect_to="")


@bp.route("/registro", methods=["POST"])
def registro():
    try:
        c = svc.crear(_datos())
    except svc.ServiceError as e:
        return jsonify(ok=False, error=str(e)), e.status
    return jsonify(ok=True, mensaje=f"¡Listo, {c.nombre.split()[0]}! Te escribiremos pronto.")


@bp.route("/clientes")
def listado():
    return render_template("clientes/index.html", clientes=svc.listar())


@bp.route("/clientes/<int:cid>/editar", methods=["GET", "POST"])
def editar(cid):
    if request.method == "POST":
        try:
            svc.actualizar(cid, _datos())
        except svc.ServiceError as e:
            return jsonify(ok=False, error=str(e)), e.status
        return jsonify(ok=True, mensaje="Cambios guardados.")
    return render_template("clientes/form.html", cliente=svc.obtener(cid), intereses=svc.intereses_activos(),
                           action=url_for("clientes.editar", cid=cid), redirect_to=url_for("clientes.listado"))


@bp.route("/clientes/<int:cid>/eliminar", methods=["POST"])
def eliminar(cid):
    svc.eliminar(cid)
    return redirect(url_for("clientes.listado"))


@bp.route("/sitemap.xml")
def sitemap():
    base = request.url_root.rstrip("/")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"  <url><loc>{base}/</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n"
           "</urlset>\n")
    return Response(xml, mimetype="application/xml")


@bp.route("/robots.txt")
def robots():
    base = request.url_root.rstrip("/")
    return Response(f"User-agent: *\nAllow: /\nDisallow: /clientes\nSitemap: {base}/sitemap.xml\n", mimetype="text/plain")
