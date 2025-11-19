# jupyter-hot-stock-scanner

### hotstockmarket

<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.6.0/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.6.0/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyCPiyVMCKblTuhBUz7pgS9QprzymzrpSSU",
    authDomain: "tpmedici.firebaseapp.com",
    databaseURL: "https://tpmedici-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "tpmedici",
    storageBucket: "tpmedici.appspot.com",
    messagingSenderId: "1071410777644",
    appId: "1:1071410777644:web:e4a37fc21753e554488b89",
    measurementId: "G-2VBE5PQXJ6"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
</script>


npm install -g firebase-tools

{
  "hosting": {
    "site": "hotstockmarket",

    "public": "public",
    ...
  }
}

firebase deploy --only hosting:hotstockmarket