<!-- Login page -->
<template>
    <div id="home">
        
        <h1>Login</h1>
        <!-- Login form -->
        <b-form @submit.prevent="login">
            <b-form-input type="text" id="email" class="input" placeholder="Email" v-model="email" required/>
            <b-form-input type="password" id="password" class="input" placeholder="Password" v-model="password" required />
            <b-button type="submit" variant="primary">Login</b-button>
        </b-form>

    </div>
</template>

<script>
export default {
    name: "Home",
    data() {
        return {
            email: "",
            password: ""
        };
    },
    components: {

    },
    methods: {
        login() {
            // Send login request to server
            fetch("http://localhost:5000/login?include_auth_token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password
                })
            }).then(response => {
                // Check if login was successful
                if (response.status === 200) {
                    // Get auth token from response
                    response.json().then(data => {
                        // Save auth token to local storage
                        localStorage.setItem("token", data.response.user.authentication_token);
                        localStorage.setItem("email", this.email);
                        this.$parent.loggedIn = true;
                        this.$parent.email = this.email;
                        // Redirect to dashboard
                        this.$router.push("/dashboard");
                    });
                } else {
                    // Login failed
                    alert("Login failed");
                }
            });
        }
    }

};
</script>

<style scoped>
.input {
    width: 400px;
    margin: 40px auto;
}
</style>
