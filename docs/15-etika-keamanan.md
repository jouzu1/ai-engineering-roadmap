# 15 — Etika, Privasi, dan Keamanan dalam AI (Bahasa Sederhana)

Tujuan:
- Memahami prinsip etika dasar dalam pengembangan AI.
- Menjaga privasi data pengguna (PII) dan kepatuhan regulasi.
- Mengamankan sistem AI dari kebocoran dan penyalahgunaan.
- Praktik sederhana untuk audit, governance, dan risk management.

Dokumen ini melengkapi aspek non-teknis yang sama pentingnya dengan kode.

------------------------------------------------------------

## 1) Prinsip Etika Dasar

- Keadilan (Fairness): Model tidak memihak kelompok tertentu. Uji bias pada data dan hasil.
- Transparansi: Jelaskan bagaimana sistem bekerja (tingkat yang sesuai). Sediakan dokumentasi dan catatan keputusan.
- Akuntabilitas: Tetapkan siapa yang bertanggung jawab atas hasil sistem.
- Kesejahteraan Pengguna: Hindari dampak negatif (mis. keputusan otomatis yang merugikan).
- Persetujuan yang Jelas (Consent): Gunakan data sesuai izin.

Praktik:
- Dokumentasikan tujuan penggunaan model, batasan, dan asumsi.
- Sediakan jalur eskalasi untuk koreksi kesalahan (human-in-the-loop bila perlu).

------------------------------------------------------------

## 2) Privasi Data dan PII

PII (Personally Identifiable Information): nama, alamat, email, nomor telepon, KTP, dll.

Praktik:
- Minimasi data: kumpulkan hanya yang perlu.
- Anonimisasi/pseudonimisasi: hapus identitas langsung; gunakan ID acak.
- Enkripsi:
  - At-rest: enkripsi file/db
  - In-transit: HTTPS/TLS
- Akses terbatas (least privilege): hanya pihak yang butuh yang bisa mengakses.
- Audit akses: catat siapa mengakses data sensitif, kapan, dan untuk apa.

Hindari:
- Memasukkan PII ke LLM publik (cloud) tanpa izin dan proteksi.
- Commit file .env atau data sensitif ke repo publik.

------------------------------------------------------------

## 3) Keamanan Aplikasi dan Infrastruktur

Rahasia (secrets):
- Simpan API key di environment variable atau secret manager (jangan hardcode).
- Gunakan .env untuk lokal, .env.example untuk berbagi struktur saja.
- Putar (rotate) kunci secara berkala.

Dependensi:
- Gunakan versi stabil, update rutin (pip/conda).
- Scan kerentanan (opsional: pip-audit).

API:
- Validasi input (Pydantic di FastAPI).
- Batasi ukuran request (payload limit).
- CORS selektif di produksi (jangan allow_origins="*").
- Rate limiting (opsional) untuk cegah abuse.

Model:
- Hindari prompt injection pada LLM (filter input, batasi kemampuan “aksi” model).
- Jangan kembalikan info sensitif (stack trace, path sistem) ke pengguna akhir.

------------------------------------------------------------

## 4) Bias dan Evaluasi yang Adil

Sumber bias:
- Data latih tidak representatif (skew), label bermasalah, sampling keliru.
- Fitur yang menjadi proxy ke atribut sensitif (ras, agama, dsb.)

Praktik:
- Evaluasi terpisah pada subgroup (per wilayah, gender bila relevan & sesuai hukum).
- Gunakan metrik tambahan selain accuracy (F1/ROC-AUC/PR-AUC).
- Catat proses pengumpulan data dan pembersihannya.

------------------------------------------------------------

## 5) Kepatuhan (Compliance) Singkat

Tergantung wilayah dan domain:
- GDPR (Uni Eropa), PDPA (beberapa negara), aturan lokal perlindungan data.
- Untuk data kesehatan, keuangan, atau anak-anak: regulasi khusus (HIPAA, COPPA, dsb.)
- Simpan bukti kepatuhan (catatan persetujuan, kebijakan privasi, DPIA bila perlu).

------------------------------------------------------------

## 6) Audit, Governance, dan Traceability

- Simpan metadata model: versi, commit hash, tanggal, parameter (MLflow).
- Simpan versi data (DVC) agar bisa “repro” hasil.
- Catat setiap rilis model ke produksi (change log).
- Dokumentasi keputusan: mengapa metrik/ambang tertentu dipilih.

------------------------------------------------------------

## 7) Penggunaan LLM secara Aman

- Filter input (hapus PII bila tidak perlu).
- Kurangi “halusinasi” dengan RAG dan sediakan sumber rujukan.
- Batasan model: beri penyangkalan (disclaimer) di UI jika saran bisa berisiko (medis/keuangan).
- Jangan gunakan LLM untuk mengambil keputusan kritikal tanpa pengawasan manusia.

------------------------------------------------------------

## 8) Insiden dan Respons

- Siapkan rencana respons insiden:
  - Siapa yang dihubungi
  - Langkah isolasi (matikan akses sementara)
  - Forensik dasar (log apa yang dicek)
  - Notifikasi ke pemangku kepentingan sesuai hukum
- Post-mortem: evaluasi akar masalah dan pencegahan ke depan.

------------------------------------------------------------

## 9) Checklist Etika & Keamanan

- [ ] Data sesuai izin dan tujuan penggunaan
- [ ] PII diproteksi (anonimisasi, enkripsi, akses terbatas)
- [ ] Rahasia disimpan sebagai environment variable/secret manager
- [ ] Validasi input dan penanganan error rapi
- [ ] Evaluasi bias dan metrik adil
- [ ] Versi data/model tercatat (DVC/MLflow)
- [ ] Dokumentasi keputusan dan dampak model
- [ ] Rencana respons insiden tersedia

Catatan khusus untuk repo ini:
- Jangan commit .env berisi kunci API. Gunakan .env.example sebagai acuan.
- Jika terlanjur memaparkan API key (mis. OpenAI), segera revoke/rotate kunci tersebut dan ganti di .env lokal Anda.

Selesai. Dengan menerapkan prinsip di atas, Anda mengurangi risiko hukum, reputasi, dan keamanan, sekaligus meningkatkan kepercayaan pengguna terhadap sistem AI Anda.
