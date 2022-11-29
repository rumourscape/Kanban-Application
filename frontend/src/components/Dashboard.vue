<template>

<div>

    <div style="max-height: 75vh; display: block; overflow-x: auto;">
        <div v-for="list in lists" class="dash">
            <coloumn :title="list"></coloumn>
        </div>
        <div style="display: inline-block; margin: 80px;">
            <h3 style="margin-bottom: 30px;"> Make a new List!</h3>
            <b-button variant="primary" @click="newList">Create List</b-button>
        </div>
    </div>

    <b-modal id="list-modal" title="Create a new List" @ok="createList" v-b-modal.modal-center>
        <b-form ref="listForm" @submit.stop.prevent="submitList">
            <b-form-group label="List Name" label-for="list-name">
                <b-form-input id="list-name" v-model="listName" :state="listName" required></b-form-input>
            </b-form-group>
        </b-form>
    </b-modal>

</div>

</template>

<script>
import Coloumn from "./coloumn.vue";

export default {
    name: "Dashboard",
    data() {
        return {
            lists: this.getLists(),
            listName: null
        }
    },
    components: {
        coloumn: Coloumn,
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
        updateLists() {
            this.lists = this.getLists();
        },
        newList() {
            this.$bvModal.show("list-modal");
        },
        createList(bvModalEvent) {
            bvModalEvent.preventDefault();

            this.submitList();
        },
        submitList() {
            // Check form is valid
            if (!this.$refs.listForm.checkValidity()) {
                return;
            }
            
            // Form is valid, so lets create the list
              fetch("http://localhost:5000/create/list", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                },
                body: JSON.stringify({
                  title: this.listName,
                }),
              }).then((res) => res.json())
                .then((data) => {
                    console.log(data);
                    if(data.status == "success") {
                        this.lists.push(this.listName);
                        this.listName = null;
                        this.$bvModal.hide("list-modal");
                    } else {
                        alert(data.error);
                    }
                })
                .catch((err) => {
                  alert(err);
                });
        }
    }
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