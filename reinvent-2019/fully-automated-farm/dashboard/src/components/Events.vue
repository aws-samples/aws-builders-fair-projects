<template>
	<div>
		<li class="greeting" v-for="(item, index) in greetings" :key="index">{{ item }}</li>
	</div>
</template>
<script>
    import {PubSub} from "aws-amplify";

    export default {
        name: "Events",
        data: function () {
            return {
                greetings: [],
				lastMessage: ""
            };
        },
        mounted: function () {
            let lastTopic = null
            PubSub.subscribe(["state/agri/#"])
                .subscribe({
                    next: data => {
                        const topic = data.value[Object.getOwnPropertySymbols(data.value)[0]].split('/')
						if(lastTopic === topic){
						    return
						}
						lastTopic = topic
						let ts = Date.now() / 1000
                        let date = new Date(ts * 1000);
                        let hours = date.getHours();
                        let minutes = "0" + date.getMinutes();
                        let seconds = "0" + date.getSeconds();
                        let formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

                        let areaName = ""
                        if (topic[2] === 'area1') {
                            areaName = "🥦🥦🥦 field"
                        } else if (topic[2] === 'area2') {
                            areaName = "🌽🌽🌽 field"
                        } else if (topic[2] === 'area3') {
                            areaName = "🥕🥕🥕 field"
                        }
                        if (topic.length >= 5) {
                            this.add("[" + formattedTime + ']\t' + topic[4] + " in " + areaName + " is in " + data.value.state + " state.")
                        } else if (topic.length >= 3) {
                            this.add("[" + formattedTime + ']\t' + areaName + " is in " + data.value.state + " state.")
                        }
                    },
                    error: error => console.error('Error', error),
                    close: () => console.log('Connection is closed'),
                })
        },
        methods: {
            add: function (message) {
                if(this.lastMessage === message){
                    return
				}
                this.greetings.unshift(message);
                if (this.greetings.length > 10) {
                    this.greetings.pop()
                }
                this.lastMessage = message
            }
        }
    };
</script>
<style>

	div {
		text-align: center;
	}

	li.greeting {
		width: 100%;
		display: inline-block;
		text-align: left;
	}
</style>
