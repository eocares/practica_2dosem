# CodeLima – Flask + MySQL (estructura estándar)

```
mi-proyecto/
├── app/
│   ├── __init__.py        create_app() – factory
│   ├── config.py          configuración por entorno (.env)
│   ├── database.py        SQLAlchemy + MySQL
│   ├── models/cliente.py  ORM: Cliente, Interes
│   ├── routes/clientes.py blueprint (CRUD, sitemap, robots)
│   ├── services/cliente_service.py  validación y lógica de negocio
│   ├── static/{css,js,img}
│   └── templates/base.html (Tailwind CDN), clientes/{index,form}.html
├── database/schema.sql
├── .env · .gitignore · app.py · requirements.txt
```

## Ejecutar local
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
mysql -u root -p < database/schema.sql            # crea BD, tablas y datos
# crea el usuario 'webapp' (ver final de schema.sql) y ajusta .env
python app.py                                     # http://localhost:5000
```
Rutas: `/` (CTA, inserta) · `/clientes` (listado) · `/clientes/<id>/editar` · `POST /clientes/<id>/eliminar` (borrado lógico) · `/sitemap.xml` · `/robots.txt`.

## Diseño físico de la BD (justificación)
| Decisión | Motivo |
|---|---|
| `intereses` + `clientes` con FK `interes_id` | Relación 1:N normalizada; alimenta el `<select>` web y el ComboBox de JavaFX. |
| PK `INT UNSIGNED AUTO_INCREMENT` | Identificador corto, único, sin negativos. |
| `VARCHAR(n)` ajustado | Ahorra espacio; teléfono como texto para no perder ceros. |
| `email UNIQUE` + `CHECK` | Evita duplicados y correos mal formados desde cualquier cliente (web, JavaFX, SQL). |
| `NOT NULL` en nombre/email/interés; `NULL` en teléfono/mensaje | Obligatorio lo necesario; opcional reduce fricción del CTA. |
| `activo TINYINT(1)` | Borrado lógico (`UPDATE ... SET activo=0`), conserva histórico. |
| `creado_en` / `actualizado` | Auditoría automática. |
| `InnoDB` + `utf8mb4` | Integridad referencial y tildes/emojis. |
| Índice `(activo, creado_en)` | Listado de activos ordenado por fecha más rápido. |

## SQL para JavaFX (JDBC)
```sql
SELECT c.id,c.nombre,c.email,c.telefono,i.nombre AS interes FROM clientes c JOIN intereses i ON i.id=c.interes_id WHERE c.activo=1;
INSERT INTO clientes(nombre,email,telefono,interes_id,mensaje) VALUES(?,?,?,?,?);
UPDATE clientes SET nombre=?,email=?,telefono=?,interes_id=?,mensaje=? WHERE id=?;
UPDATE clientes SET activo=0 WHERE id=?;
```

## Gitflow + Conventional Commits (3 commits por estudiante)
```bash
git init && git add . && git commit -m "chore: estructura inicial estándar Flask"
git branch -M main && git checkout -b develop
git checkout -b feature/estudiante1-formulario
git commit -am "feat(clientes): agrega formulario CTA conectado a MySQL"
git commit -am "style(ui): implementa diseño responsive con Tailwind"
git commit -am "feat(js): agrega animaciones typing y contadores"
git checkout develop && git merge --no-ff feature/estudiante1-formulario
git checkout -b release/1.0.0 && git checkout main && git merge --no-ff release/1.0.0 && git tag v1.0.0
```
Cada integrante repite con su propia rama `feature/...`.

## Despliegue en AWS EC2
**Security Group (inbound):** HTTP 80 y HTTPS 443 → `0.0.0.0/0`; SSH 22 y MySQL 3306 → **My IP**.
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv nginx mysql-server git
git clone <tu-repo> mi-proyecto && cd mi-proyecto
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
# MySQL remoto
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf && sudo systemctl restart mysql
sudo mysql < database/schema.sql
sudo mysql -e "CREATE USER 'webapp'@'%' IDENTIFIED BY 'TuClaveSegura1!'; GRANT SELECT,INSERT,UPDATE ON codelima.* TO 'webapp'@'%'; FLUSH PRIVILEGES;"
# .env: FLASK_ENV=production, DB_HOST=localhost, DB_USER=webapp, DB_PASSWORD=...
gunicorn -w 2 -b 127.0.0.1:8000 app:app --daemon
sudo tee /etc/nginx/sites-available/default <<'CONF'
server { listen 80; location / { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; } }
CONF
sudo systemctl restart nginx
```
**Workbench:** Hostname = IP pública EC2, puerto 3306, usuario `webapp` y su contraseña. Verifica con `SELECT * FROM clientes;`.

**Sitemap:** `/sitemap.xml` (protocolo sitemaps.org, UTF-8, `<loc>` absoluta, `<lastmod>` ISO 8601), declarado en `/robots.txt`; envíalo en Google Search Console.
