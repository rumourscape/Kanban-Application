<!-- Kanban coloumn -->
<template>
    <div class="coloumn" style="background-color: honeydew">
        <b-dropdown :text="title" variant="primary" right class="m-md-2">
            <b-dropdown-item variant="warning" v-b-modal="editListModal" >Edit</b-dropdown-item>
            <b-dropdown-item variant="danger" @click="deleteList">Delete</b-dropdown-item>
        </b-dropdown>
        <hr/>
        <div class="lists">
            <b-card v-if="!empty" v-for="card in cards" :title="card" class="card" style="background-color: aliceblue;">
                <b-button variant="danger" size="sm" @click="deleteCard(card)" class="button">Delete</b-button>
            </b-card>

            <h3 v-if="empty">No cards</h3>
        </div>
        
        <hr/>
        <b-button variant="primary" v-b-modal="cardModal">Add Card</b-button>

        <b-modal :id="cardModal" title="Create a new Card" @ok="submitCard" centered static>
            <b-form ref="cardForm" @submit.stop.prevent="submitCard">
                <b-form-group label="Card Name" label-for="card-name">
                    <b-form-input id="card-name" v-model="cardName" :state="cardName" required></b-form-input>
                </b-form-group>
            </b-form>
        </b-modal>

        <b-modal :id="editListModal" title="Edit List" @ok="submitEditedList" centered static>
            <b-form ref="listForm" @submit.stop.prevent="submitEditedList">
                <b-form-group label="List Name" label-for="list-name">
                    <b-form-input id="list-name" v-model="listName" :state="listName" required></b-form-input>
                </b-form-group>
            </b-form>
        </b-modal>
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
                empty: true,
                cards: this.getCards(),
                cardModal: "card-"+this.title,
                editListModal: "editList-"+this.title,
                cardName: null,
                listName: null,
            }
        },
        methods: {
            getCards() {
                fetch("http://localhost:5000/get/cards?" + new URLSearchParams({'list': this.title}) , {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        }
                })  .then(res => res.json())
                    .then(data => {
                        console.log(data);
                        if(data.cards.length != 0) {
                            this.empty = false;
                            this.cards = data.cards;
                        } else {
                            this.empty = true;
                            this.cards = []
                        }
                    })
            },
            submitCard() {
                // Check form is valid
                if (!this.$refs.cardForm.checkValidity()) {
                    return;
                }
                
                // Form is valid, so lets create the list
                fetch("http://localhost:5000/create/card", {
                    method: "POST",
                    headers: {
                    "Content-Type": "application/json",
                    "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        },
                    body: JSON.stringify({
                        list: this.title,
                        title: this.cardName,
                        }),
                    })  .then((res) => res.json())
                        .then((data) => {
                            console.log(data);
                            if(data.status == "success") {
                                this.cards.push(this.cardName);
                                this.empty = false;
                                this.cardName = null;
                                this.$bvModal.hide(this.cardModal);
                            } else {
                                alert(data.error);
                            }
                        })
                        .catch((err) => {
                            alert(err);
                        });
            },
            submitEditedList() {
                // Check form is valid
                if (!this.$refs.listForm.checkValidity()) {
                    return;
                }

                console.log(this.listName);

                fetch("http://localhost:5000/edit/list", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        },
                    body: JSON.stringify({
                        list: this.title,
                        title: this.listName
                        })
                    })  .then((res) => res.json())
                        .then((data) => {
                            console.log(data);
                            if(data.status == "success") {
                                this.$bvModal.hide(this.editListModal);
                                this.title = this.listName;
                            } else {
                                alert(data.error);
                            }
                        })
                        .catch((err) => {
                            alert(err);
                        });
            },
            deleteList() {
                console.log(this.title);
                fetch("http://localhost:5000/delete/list", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        },
                    body: JSON.stringify({ title: this.title })
                    }).then(res => res.json())
                      .then(data => {
                        console.log(data);
                        if (data.status == "success") {
                            this.$parent.getLists();
                            this.$parent.$forceUpdate();
                        } else {
                            alert(data.message);
                        }
                      })
            },
            deleteCard(card) {
                fetch("http://localhost:5000/delete/card", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        },
                    body: JSON.stringify({ title: card, list: this.title})
                }).then(res => res.json())
                  .then(data => {
                    console.log(data);
                    if (data.status == "success") {
                        this.cards.splice(this.cards.indexOf(card), 1);
                        if(this.cards.length == 0) {
                            this.empty = true;
                        }
                        this.$forceUpdate();
                    } else {
                        alert(data.message);
                    }
                  })
            }
        }
    };
</script>

<style scoped>
    .coloumn {
        margin: 10px 20px;
        padding: 10px 20px;
        border: 1px solid #000000;
        border-radius: 5px;
        display: grid;
        flex: content;

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