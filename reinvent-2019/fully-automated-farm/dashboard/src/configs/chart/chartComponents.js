import {PubSub} from "aws-amplify";
import {chartOptionsChart} from "./chartOptions";

const chartExportComponents = {
	name: 'Chart',
	props: {
		column: {
			type: String,
			required: true
		}
	},
	data: function () {
		return {
			series: [],
			chartOptionsChart: chartOptionsChart
		}
	},
	mounted: async function () {
		let columnNo = parseInt(this.column)
		let areaNo = columnNo + 1
		const topicName = "data/agri/area" + areaNo + "/moisture/#"
		let dates = new Array(9)
		for (let i = 0; i < 9; i++) {
			dates[i] = {
				name: "No." + (i + 1),
				data: []
			}
		}
		if (localStorage.getItem("dates") !== null) {
			dates = JSON.parse(localStorage.getItem("dates"))
		}
		const topic = PubSub.subscribe(topicName)
		let parseSensorId = (thingName) => parseInt(thingName.replace("moisture", "")) - 1
		let lastUpdateTime = Date.now()
		topic.subscribe({
			next: data => {
				const topic = data.value[Object.getOwnPropertySymbols(data.value)[0]].split('/')
				let sensorId = parseSensorId(topic[topic.length - 1])
				dates[sensorId].data.push([data.value.ts, data.value.moisture])
				if (dates[sensorId].data.length > 50) {
					dates[sensorId].data.shift()
				}
				localStorage.setItem("dates", JSON.stringify(dates))
				// console.log('sub', dates)

				let now = Date.now()
				if (now - lastUpdateTime > 1000) {
					lastUpdateTime = now

					const map = this.$refs.chart
					// console.log("columnNo: "+columnNo)
					if (columnNo === 0 && sensorId >= 0 && sensorId <= 2) {
						map.updateSeries(dates.slice(0, 3))
					}
					if (columnNo === 1 && sensorId >= 3 && sensorId <= 5) {
						map.updateSeries(dates.slice(3, 6))
					}
					if (columnNo === 2 && sensorId >= 6 && sensorId <= 8) {
						map.updateSeries(dates.slice(6, 9))
					}

				}

			},
			error: error => console.error('Error', error),
			close: () => console.log('Connection is closed'),
		})
		console.log('Subscribe', topicName)
	}
}

export {chartExportComponents}
