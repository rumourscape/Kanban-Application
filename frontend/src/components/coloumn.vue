<!-- Kanban coloumn -->
<template>
    <div class="coloumn" style="background-color: honeydew">
        <b-dropdown :text="title" variant="primary" right class="m-md-2">
            <b-dropdown-item variant="danger">Delete</b-dropdown-item>
        </b-dropdown>
        <hr/>
        <div class="lists">
            <b-card v-if="!empty" v-for="card in cards"  :title="card" class="card" style="background-color: aliceblue;">
                <b-button variant="danger" size="sm" @click="" class="button">Delete</b-button>
            </b-card>
        </div>
        
        <hr/>
        <b-button variant="primary" @click="">Add Card</b-button>
    </div>
</template>

<script>
    export default {
        name: "Coloumn",
        props: {
            title: String,
        },
        data() {
            return {
                username: this.$parent.username,
                empty: false,
                cards: ["hi","a","b","c","d","e","f","g"]
            }
        },
        components: {
        },
    };
</script>

<style scoped>
    .coloumn {
        margin: 10px 20px;
        padding: 10px 20px;
        border: 1px solid #000000;
        border-radius: 5px;
        display: grid;
        flex: auto;

    }
    .lists {
        margin-bottom: 10px;
        overflow-y: auto;
        flex: auto;
    }
    .card {
        margin: 10px;
    }

    .button {
        margin: 5px;
    }
</style>