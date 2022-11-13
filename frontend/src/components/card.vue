<template>
    <b-card :title="title" class="card">
        <b-card-text> {{ description }} </b-card-text>
    </b-card>
</template>

<script>
export default {
    el: "#card",
    props: {
        title: String,
        description: String,
    },
    components: {
    },
};
</script>

<style scoped>
.card {
    color: rgb(184, 229, 244);
    background-color: rgb(0, 0, 0);
    border-radius: 5px;
    border-color: rgb(19, 143, 252);
    border-style: solid;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
    margin: 50px auto;
    padding: 20px;
    width: 300px;
}
</style>