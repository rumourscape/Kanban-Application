<!-- Kanban coloumn -->
<template>
    <div class="coloumn" style="background-color: honeydew">
        <b-dropdown :text="title" variant="primary" right class="m-md-2">
            <b-dropdown-item variant="primary" @click="exportList">Export</b-dropdown-item>
            <b-dropdown-item variant="warning" v-b-modal="editListModal" >Edit</b-dropdown-item>
            <b-dropdown-item variant="danger" @click="deleteList">Delete</b-dropdown-item> 
        </b-dropdown>
        <hr/>
        <div class="lists">
            <b-card v-if="!empty" v-for="card in cards" :title="card.title" class="card" footer-tag="footer">
                
                <b-collapse :id="card.title">
                    <b-card style="background-color: lightpink">
                        {{card.content}}
                        <hr />
                        Deadline: {{card.deadline}}
                        <hr />
                        Completed: {{card.completed}}
                    </b-card>
                </b-collapse>

                <b-modal :id="card.title" title="Edit Card" @ok="submitEditedCard(card)" centered static>
                    <b-form ref="editCardForm" @submit.stop.prevent="submitEditedCard">
                        <b-form-input id="card-name" v-model="cardName" required />
                        <hr/>
                        <b-form-input id="card-content" v-model="cardContent" required />
                        <hr/>
                        <b-form-input id="card-list" v-model="cardList" required />
                        <hr/>
                        <b-form-checkbox id="card-completed" v-model="cardCompleted" switch> Completed </b-form-checkbox>
                        <hr/>
                        <b-form-group label="Deadline"></b-form-group>
                        <b-calendar v-model="cardDate" :min="minDate" required />
                    </b-form>
                </b-modal>

                <template #footer>
                    <b-button variant="info" v-b-toggle="card.title" size="sm" class="button">More</b-button>
                    <b-button variant="warning" size="sm" @click="showEditCardModal(card)" class="button">Edit</b-button>
                    <b-button variant="danger" size="sm" @click="deleteCard(card)" class="button">Delete</b-button>
                </template>
            </b-card>

            <h3 v-if="empty">No cards</h3>
        </div>
        
        <hr/>
        <b-button variant="primary" v-b-modal="cardModal">Add Card</b-button>

        <!-- Modals -->
        <b-modal :id="cardModal" title="Create a new Card" @ok="submitCard" centered static>
            <b-form ref="cardForm" @submit.stop.prevent="submitCard">
                <b-form-input id="card-name" v-model="cardName" placeholder="Card Name" required />
                <hr/>
                <b-form-input id="card-content" v-model="cardContent" placeholder="Card Content" required />
                <hr/>
                <b-form-group label="Deadline"></b-form-group>
                <b-calendar v-model="cardDate" :min="minDate" required />
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
                cardContent: null,
                cardDate: null,
                cardCompleted: false,
                cardList: null,
                listName: null,
                minDate: new Date(),
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
                    alert("Please fill all the fields");
                    return;
                }

                console.log(this.cardDate);
                
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
                        content: this.cardContent,
                        deadline: this.cardDate
                        }),
                    })  .then((res) => res.json())
                        .then((data) => {
                            console.log(data);
                            if(data.status == "success") {
                                this.getCards();
                                this.empty = false;
                                this.cardName = null;
                                this.cardContent = null;
                                this.cardDate = null;
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
            showEditCardModal(card) {
                this.cardName = card.title;
                this.cardContent = card.content;
                this.cardDate = card.deadline;
                this.cardCompleted = card.completed;
                this.cardList = this.title;

                this.$bvModal.show(card.title);
            },
            submitEditedCard(card) {
                // Check form is valid
                if (!this.$refs.cardForm.checkValidity()) {
                    return;
                }
                console.log(this.cardCompleted);

                fetch("http://localhost:5000/edit/card", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        },
                    body: JSON.stringify({
                        "id": card.id,
                        "list": this.cardList,
                        "title": this.cardName,
                        "content": this.cardContent,
                        "deadline": this.cardDate,
                        "completed": this.cardCompleted
                    })
                }).then((res) => res.json())
                  .then((data) => {
                    console.log(data);
                    if(data.status == "success") {
                        if (this.cardList != this.title) {
                            this.$parent.updateLists();
                        }
                        else {
                            this.getCards();
                            this.cardName = null;
                            this.cardContent = null;
                            this.cardDate = null;
                            this.cardCompleted = false;
                            this.cardList = null;
                            this.$bvModal.hide(this.cardModal);
                        }
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
                    body: JSON.stringify({ title: card.title, list: this.title})
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
            },
            exportList() {
                fetch("http://localhost:5000/export?" + new URLSearchParams({'list': this.title}), {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        }
                })  .then( res => res.blob() )
                    .then( blob => {
                        var file = window.URL.createObjectURL(blob);
                        window.location.assign(file);
                    })
                    .then( this.$parent.triggerExportAlert() )
            },
            getId(card) {
                return card.id
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
        background-color: aliceblue;
    }

    .button {
        margin: 5px;
    }
</style>