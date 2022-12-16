<template>
    <b-card :title="list" class="card">
                <hr/>
                <b-card-text>
                    Number of cards: {{ cards.length }}
                    <br/>
                    Completed tasks: {{ completedCards() }}
                    <br/>
                    Past deadline: {{ pastDeadline() }}
                </b-card-text>
            </b-card>
</template>

<script>
import moment from "moment";

export default {
    name: "SummaryCard",
    props: {
        list: String,
    },
    data() {
        return {
            cards: this.getCards(),
        }
    },
    methods: {
        getCards() {
                fetch("http://localhost:5000/get/cards?" + new URLSearchParams({'list': this.list}) , {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "AUTHENTICATION-TOKEN": localStorage.getItem("token")
                        }
                })  .then(res => res.json())
                    .then(data => {
                        console.log(data);
                        if(data.cards.length != 0) {
                            this.cards = data.cards;
                        } else {
                            this.cards = []
                        }
                    })
            },
        completedCards() {
            let completed = 0;
            for(let i = 0; i < this.cards.length; i++) {
                if(this.cards[i].completed) {
                    completed++;
                }
            }
            return completed;
        },
        pastDeadline() {
            let past = 0;
            let date;
            for(let i = 0; i < this.cards.length; i++) {
                date = moment(this.cards[i].deadline).format("YYYY-MM-DD");
                if(date > moment()) {
                    past++;
                }
            }
            return past;
        }
    }
}
</script>