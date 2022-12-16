<template>
    <div>
        <h1> Summary </h1>
        <div v-for="list in lists">
            <Scard :list="list" />
        </div>
        

    </div>
</template>

<script>
import SummaryCard from "./summary-card.vue";

export default {
    name: "Summary",
    data() {
        return {
            lists: this.getLists(),
        }
    },
    components: {
        Scard: SummaryCard,
    },
    methods: {
        getLists() {
            fetch("http://localhost:5000/get/lists", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                    }
                }).then(res => res.json())
                .then(data => {
                    if(data.lists.length != 0) {
                        this.lists = data.lists;
                    } else {
                        this.lists = []
                    }
                })
                .catch(err => alert(err));
        },
    }
};
</script>

<style scoped>
.card {
        margin: 50px;
        width: 1000px;
        text-align: left;
        background-color: lightgray;
    }
</style>