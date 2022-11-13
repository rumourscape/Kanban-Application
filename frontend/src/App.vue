<template>
  <div id="app">
    <div>
      <h1 style="color:darkslateblue">KANBAN</h1>
    </div>
      <hr/>
    <div v-if="loggedIn">
      <h5 class="navleft">Hi {{email}},</h5>
      <b-button to="/dashboard" style="margin: auto 20px;"> Dashboard </b-button>
      <b-button to="/about"> About </b-button>
      <h5 class="navright"><b-button variant="danger" @click="logout"> Logout </b-button></h5>
      <hr/>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
  el: "#app",
  name: "App",
  data() {
    return {
      loggedIn: false,
      email: "",
    };
  },
  components: {
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("email");
      this.loggedIn = false;
      this.$router.push("/");
    },
  },
  created() {
    // Check if user is logged in
    let token = localStorage.getItem("token");
    console.log(token);
    if (token) {
      fetch("http://localhost:5000/verify-token", {
        method: "GET",
        headers: {
          "AUTHENTICATION-TOKEN": token,
        },
      }).then((response) => {
        if (response.status === 200) {
          this.email = localStorage.getItem("email");
          this.loggedIn = true;
          this.$router.push("/dashboard");
        }
      });
    }
  },
};
</script>

<style scoped>
#app {
  font-family: sans-serif;
  text-align: center;
  color: #000000;
  margin-top: 60px;
}

.navleft {
  display: inline-flex;
  vertical-align: middle;
  float: left;
  margin-left: 10%;
}

.navright {
  display: inline-flex;
  vertical-align: middle;
  float: right;
  margin-right: 10%;
}
</style>