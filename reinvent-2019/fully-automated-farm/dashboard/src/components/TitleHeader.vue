<template>
	<div>
		<div id="title">
			<h1>{{title}}</h1>
		</div>
	</div>
</template>

<script>
    import {PubSub} from "aws-amplify";

    export default {
        name: "TitleHeader",
        data: function () {
            return {
                title: "*** Agri Dashboard ***"
            }
        },
        mounted: async function () {

            PubSub.subscribe("data/agri/area1/light/light1")
                .subscribe({
                    next: data => {
                        const weather = data.value.weather
                        if (weather === "fine") {
                            this.title = "🌈🌈🌈 Agri Dashboard 🌈🌈🌈"
                        } else {
                            this.title = "☔☔☔ Agri Dashboard ☔☔☔"

                        }
                    },
                    error: error => {
                        console.error('Error', error)
                        location.reload()
                    },
                    close: () => console.log('Connection is closed'),
                })
        },
    }
</script>

<style scoped>
	h1 {
		font-size: 30px;
		color: white;
	}

	div {
		width: 100%;
		height: 40px;
	}

</style>
