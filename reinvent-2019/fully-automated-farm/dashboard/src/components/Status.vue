<template>
	<div>
		<h3>{{title}}</h3>
		<div id="status" class="center" v-bind:style="{background : stateColor}">{{currentState}}</div>
	</div>
</template>

<script>
    import {PubSub} from "aws-amplify";

    export default {
        name: "Status",
        props: ['title', 'column'],
        data: () => {
            return {
                currentState: "Unknown",
                stateColor: "gray"
            }
        },
        mounted: async function () {

            const areaId = parseInt(this.column) + 1
            PubSub.subscribe("state/agri/area" + areaId + "/pump/#")
                .subscribe({
                    next: data => {
                        const pumpState = data.value.state
                        if (pumpState === "ON") {
                            this.currentState = "💧Watering"
                            this.stateColor = "deepskyblue"
                        } else if (pumpState === "OFF") {
                        }
                    },
                    error: error => console.error('Error', error),
                    close: () => console.log('Connection is closed'),
                })

            PubSub.subscribe("state/agri/area" + areaId)
                .subscribe({
                    next: data => {
                        const state = data.value.state
                        console.log(state)
                        if (state === "no_water") {
                            this.currentState = "😨No Water"
                            this.stateColor = "red"
                        } else if (state === "less_water" && this.currentState !== "💧Watering") {
                            this.currentState = "Less Water"
                            this.stateColor = "orange"
                        } else if (state === "full_water") {
                            this.currentState = "🌱Good"
                            this.stateColor = "limegreen"
                        }
                    },
                    error: error => console.error('Error', error),
                    close: () => console.log('Connection is closed'),
                })

        },

    }
</script>

<style scoped>
	h3 {
		font-size: 15px;
		margin-bottom: 5px;
		margin-top: 5px;
	}

	div {
		text-align: center;
	}

	#status {
		width: 90%;
		height: 40px;
		background: #999999;
		display: inline-block;
		margin-bottom: 10px;
		font-size: 12px;
	}

	.center {
		line-height: 40px; /* same as height! */
	}
</style>
