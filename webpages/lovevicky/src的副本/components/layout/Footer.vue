<template>
  <footer class="footer glass">
    <div>
      © 2025 Face Age Estimation Platform | Contact: <a href="mailto:contact@faceage.com" class="email">contact@faceage.com</a>
    </div>
    <div class="privacy">
      <a href="#" class="privacy-link">Privacy Statement</a>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  padding: 22px 0 15px 0;
  text-align: center;
  font-size: 15.5px;
  color: #e8e1fd;
  background: rgba(40, 16, 58, 0.86);
  border-top: 1.5px solid #a18fff55;
  border-radius: 0 0 18px 18px;
  box-shadow: 0 -3px 22px #7f3eb644;
  letter-spacing: 0.05em;
}

.footer .email {
  color: #c7a9ff;
  text-decoration: underline wavy #a08fff;
  transition: color 0.18s;
}
.footer .email:hover {
  color: #ff73e2;
}

.privacy {
  margin-top: 8px;
  font-size: 14px;
}
.privacy-link {
  color: #8ef8ff;
  text-decoration: underline dashed #d9b9ff;
  transition: color 0.19s;
}
.privacy-link:hover {
  color: #e48bff;
}
</style>
