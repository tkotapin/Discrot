# update dulu
  sudo apt update && apt upgrade

# Clone
  git clone https://github.com/tkotapin/Discrot.git
  cd Discrot

# Install dulu requirements.txt nya
  pip install -r requirements.txt

# Edit file .env
  nano .env
  kalo ga kebaca .env dari repo, buat baru aja
  isi token personal (jangan token bot), isi ID channel & isi user ID biar gak bales chat diri sendiri
  untuk personal token bisa login discord di web di homepage inspect element
  masuk ke tab application > localstorage trus cari Token copi value nya paste ke .env, SAVE
  Edit file .env isinya :
  DISCORD_TOKEN buka discrot web inspect di tab aplikasi cari token
  CHANNEL_ID buka chat room copy no ID  /palingbelakang
  BOT_USER_ID sama inspect element cari ID di search bar

  DISCORD_TOKEN=
  CHANNEL_ID=
  BOT_USER_ID=
  
  tinggal run discrot.py
