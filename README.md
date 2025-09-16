# 💾 VM Backup & Monitoring Dashboard

A **cloud-enabled backup and monitoring solution** for VMware/VMs, built with **FastAPI, PostgreSQL, Docker, and AWS S3/Glacier**.

## 🚀 Features

* ✅ Automated VM backups with scheduling
* ☁️ AWS S3 + Glacier integration for long-term storage
* 📊 Backup history & monitoring
* 🐳 Dockerized deployment
* 🔐 Role-based access (planned)

## 🛠 Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL
* **Task Scheduler:** APScheduler
* **Cloud:** AWS S3 + Glacier
* **Infrastructure:** Linux, ESXi, Paramiko, vmkfstools
* **Containers:** Docker + Docker Compose

## ⚙️ Setup

### 1️⃣ Clone the repo

```bash
git clone https://github.com/Boulaz2002/backup-dashboard.git
cd backup-dashboard
```

### 2️⃣ Configure `.env`

```env
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=xxxx
AWS_DEFAULT_REGION=us-east-2
AWS_S3_BUCKET=my-backup-bucket

ESXI_HOST=192.168.x.x
ESXI_USER=root
ESXI_PASS=yourpassword
ESXI_DATASTORE=datastore1
```

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

### 4️⃣ Access

* API Docs → [http://localhost:8000/docs](http://localhost:8000/docs)
* Database → `postgres://postgres:postgres@backup_db:5432/backupdb`

## 📡 API Endpoints

### Manual Backup

```http
POST /backup/now?vm_name=VM1
```

### Schedule Backup

```http
POST /backup/schedule
```

```json
{
  "vm_name": "VM1",
  "hour": 2,
  "minute": 0,
  "day_of_week": "*"
}
```

### List Scheduled Jobs

```http
GET /backup/schedule/jobs
```

### Backup History

```http
GET /backup/history
```

## 🗼 Screenshots

(Add images of dashboard, API usage in Postman, backup history, etc.)

## 📌 Roadmap

* [ ] Add Web UI for monitoring
* [ ] Role-based authentication (JWT)
* [ ] Email/Slack notifications for failures
* [ ] Multi-datastore support

---

👨‍💻 Developed by [Benjamin Boule Fogang](https://github.com/Boulaz2002)
