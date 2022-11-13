<template>

<div>

    <div style="max-height: 75vh; display: block; overflow-x: auto;">
        <div v-for="list in lists" class="dash">
            <coloumn :title="list"></coloumn>
        </div>
    </div>

    <div style="display: inline-block; margin: 80px;">
        <h3 style="margin-bottom: 30px;"> Make a new List!</h3>
        <b-button variant="primary" @click="">Create List</b-button>
    </div>

</div>

</template>

<script>
import Coloumn from "./coloumn.vue";

export default {
    name: "Dashboard",
    data() {
        return {
            username: this.$parent.username,
            lists: ["to-do","In Progress", "done","b"]
        }
    },
    components: {
        coloumn: Coloumn
    },
};
</script>

<style scoped>
.dash {
    height: 75vh;
    width: 25%;
    display: flex;
    float: left;
}
</style>