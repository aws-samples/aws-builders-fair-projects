<template>
	<div id="app">
		<TitleHeader/>
		<ul class="col3">
			<li>
				<Status title="🥦Radish🥦" column="0"/>
				<Heatmap column="0"/>
			</li>
			<li>
				<Status title="🌽Corn🌽" column="1"/>
				<Heatmap column="1"/>
			</li>
			<li>
				<Status title="🥕Carrot🥕" column="2"/>
				<Heatmap column="2"/>
			</li>
		</ul>
	</div>
</template>
<script>
    import TitleHeader from './components/TitleHeader'
    import Status from './components/Status'
    import Heatmap from './components/Heatmap'
    import Chart from './components/Chart'
    import Events from './components/Events'

    import awsconfig from './aws-exports'
    import {iotEndpoint} from './configs/endpoint'
    import Amplify from 'aws-amplify'
    import {AWSIoTProvider} from '@aws-amplify/pubsub/lib/Providers'

    Amplify.addPluggable(new AWSIoTProvider(iotEndpoint))
    Amplify.configure(awsconfig)

    export default {
        name: 'AppRpi',
        components: {
            Heatmap, Chart, TitleHeader, Status, Events
        },
    }
</script>

<style>
	#app {
		font-family: 'Press Start 2P', cursive;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		color: #2c3e50;
		margin-top: 10px;
	}

	body {
		background: #7F7 url("./assets/agri-design.png");
	}

	.col3 {
		display: flex;
	}

	.col3 li {
		width: calc(100% / 3);
	}

	ul,
	li {
		padding-left: 0;
		margin-top: 0;
		margin-bottom: 0;
		list-style: none;
	}

	li {
		background: #fff;
		text-align: center;
		border: 3px solid #aaa;
	}


</style>
