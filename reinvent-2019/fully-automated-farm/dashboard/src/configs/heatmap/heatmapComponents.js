import {chartOptionsHeatMap} from './chartOptions'
import {PubSub} from "aws-amplify";

const heatmapExportComponents = {
	name: 'Main',
	props: {
		column: {
			type: String,
			required: true
		}
	},
	data: function () {
		return {
			series: [],
			chartOptionsHeatMap: chartOptionsHeatMap,
		}
	},
	mounted: async function () {
		let columnNo = parseInt(this.column)
		let heatmaps = []
		for (let j = 0; j < 3; j++) {
			let heatmap = new Array(3)
			for (let i = 0; i < 3; i++) {
				let name = i + j * 3 + 1
				heatmap[i] = {
					name: "s" + name,
					data: [{
						x: '',
						y: 0
					}]
				}
			}
			heatmaps.push(heatmap)
		}
		let areaNo = columnNo + 1
		let parseSensorId = (thingName) => parseInt(thingName.replace("moisture", "")) - 1

		let lastUpdateTime = Date.now()
		PubSub.subscribe("data/agri/area" + areaNo + "/moisture/#")
			.subscribe({
				next: data => {
					const topic = data.value[Object.getOwnPropertySymbols(data.value)[0]].split('/')
					let sensorId = parseSensorId(topic[topic.length - 1])
					let column = sensorId % 3
					let row = Math.floor(sensorId / 3)
					heatmaps[row][column].data[0].y = data.value.moisture
					if (sensorState[column] === "Drying") {
						heatmaps[row][column].name = "Dry"
					} else if (sensorState[column] === "Moist") {
						heatmaps[row][column].name = "Wet"
					} else if (sensorState[column] === "Sensor-Down") {
						heatmaps[row][column].name = "😔"
					} else {
						heatmaps[row][column].name = "?"
					}

					let now = Date.now()
					if (now - lastUpdateTime > 1000) {
						const map = this.$refs.heatmap
						lastUpdateTime = now
						map.updateSeries(heatmaps[columnNo])
					}
				},
				error: error => console.error('Error', error),
				close: () => console.log('Connection is closed'),
			})

		let sensorState = ["Dry", "Dry", "Dry"]
		PubSub.subscribe("state/agri/area" + areaNo + "/moisture/#")
			.subscribe({
				next: data => {
					const topic = data.value[Object.getOwnPropertySymbols(data.value)[0]].split('/')
					let sensorId = parseSensorId(topic[topic.length - 1])
					let column = sensorId % 3
					sensorState[column] = data.value.state
				},
				error: error => console.error('Error', error),
				close: () => console.log('Connection is closed'),

			})


	},
}

export {heatmapExportComponents}
