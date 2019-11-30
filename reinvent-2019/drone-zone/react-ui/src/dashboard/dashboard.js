import React from 'react';
import Amplify, { Auth, PubSub } from 'aws-amplify';
import IoT from 'aws-sdk/clients/iot';
import { AWSIoTProvider } from '@aws-amplify/pubsub/lib/Providers';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import { Grid, Segment, Button, Statistic, Header, Table, Dropdown, Icon } from 'semantic-ui-react'
import { toast } from 'react-semantic-toasts';
import Config from '../config';

var subscriptions = []

// Apply plugin with configuration
Amplify.addPluggable(new AWSIoTProvider({
    aws_pubsub_region: Config.region,
    aws_pubsub_endpoint: Config.wss_endpoint,
}));

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            telemetry: {},
            name: this.props.name,
            thingName: this.props.thingName,
            message: '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A0M++f9/AIYRBgoiIqKDCiPKgPvC+95tJBTV+dTSU1VdnXmdCKJ68qx5Pal1x9nqnpdffvnjhYkAAQIECBAgQGAagXun6amOEiBAgAABAgQInAkIgAYCAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJmAADhZwXWXAAECBAgQICAAGgMECBAgQIAAgckEBMDJCq67BAgQIECAAAEB0BggQIAAAQIECEwmIABOVnDdJUCAAAECBAgIgMYAAQIECBAgQGAyAQFwsoLrLgECBAgQIEBAADQGCBAgQIAAAQKTCQiAkxVcdwkQIECAAAECAqAxQIAAAQIECBCYTEAAnKzgukuAAAECBAgQEACNAQIECBAgQIDAZAIC4GQF110CBAgQIECAgABoDBAgQIAAAQIEJhMQACcruO4SIECAAAECBARAY4AAAQIECBAgMJnA5yfrr+4SuPIC//nPfxZ//etfu/348pe/vPj85/f/P+uPPvpo8fHHH39mn/fee+/igQce+EzbLv/I9v785z8vPvzww8U//vGPxb/+9a/Ffffdt/jiF7+4ePTRRxcPPvjgLps7mWVTm7/97W9n//39738/61fq8qUvfWmRz/vvv3/xhS98Ye/He+hxMWq99l4IGyRwRQT2/01xRTruMAlcVYHf//73i1u3bp07/M997nOLl1566Vz73TYk0PzsZz87t5kEmRdffPFc+zYN77///uI3v/nNWfDrLf+73/3uLFzeuHHjLDD1ljm1tgSwX//614vbt2+fO7SE3Dbdc889i+vXry+uXbu2yN/7mg45Lkas177cbYfAVRVwCfiqVs5xTymQkPGHP/yh2/ennnpqkRC47ynBYp9Tjv+NN94ow1/b11/+8pez4JmzhKc+JST/9Kc/7Ya/1WPPmbS333578frrr5+dHVydf5F/H3JcjFivixhbh8BoAgLgaBXVn6EF3nvvvcW///3vc31M8MsZpX1P//znPxd//OMf97bZP/3pT2dnybbd4H//+9+zsJhLqac6JdAl0O56jB988MHitddeO3dp/SL9PNS4GLFeF/G1DoERBQTAEauqT0MKJAzl0mhvSvg7xL1/OfuTgLOP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RhUQAEetrH4RIECAAAECBAoBAbCA0UyAAAECBAgQGFVAABy1svpFgAABAgQIECgEBMACRjMBAgQIECBAYFQBAXDUyuoXAQIECBAgQKAQEAALGM0ECBAgQIAAgVEFBMBRK6tfBAgQIECAAIFCQAAsYDQTIECAAAECBEYVEABHrax+ESBAgAABAgQKAQGwgNFMgAABAgQIEBhVQAActbL6RYAAAQIECBAoBATAAkYzAQIECBAgQGBUAQFw1MrqFwECBAgQIECgEBAACxjNBAgQIECAAIFRBQTAUSurXwQIECBAgACBQkAALGA0EyBAgAABAgRGFRAAR62sfhEgQIAAAQIECgEBsIDRTIAAAQIECBAYVUAAHLWy+kWAAAECBAgQKAQEwAJGMwECBAgQIEBgVAEBcNTK6hcBAgQIECBAoBAQAAsYzQQIECBAgACBUQUEwFErq18ECBAgQIAAgUJAACxgNBMgQIAAAQIERhUQAEetrH4RIECAAAECBAoBAbCA0UyAAAECBAgQGFVAABy1svpFgAABAgQIECgEBMACRjMBAgQIECBAYFQBAXDUyuoXAQIECBAgQKAQEAALGM0ECBAgQIAAgVEFBMBRK6tfBAgQIECAAIFCQAAsYDQTIECAAAECBEYVEABHrax+ESBAgAABAgQKAQGwgNFMgAABAgQIEBhVQAActbL6RYAAAQIECBAoBATAAkYzAQIECBAgQGBUAQFw1MrqFwECBAgQIECgEBAACxjNBAgQIECAAIFRBQTAUSurXwQIECBAgACBQkAALGA0EyBAgAABAgRGFRAAR62sfhEgQIAAAQIECgEBsIDRTIAAAQIECBAYVUAAHLWy+kWAAAECBAgQKAQEwAJGMwECBAgQIEBgVAEBcNTK6hcBAgQIECBAoBAQAAsYzQQIECBAgACBUQUEwFErq18ECBAgQIAAgUJAACxgNBMgQIAAAQIERhUQAEetrH4RIECAAAECBAoBAbCA0UyAAAECBAgQGFVAABy1svpFgAABAgQIECgEBMACRjMBAgQIECBAYFQBAXDUyuoXAQIECBAgQKAQEAALGM0ECBAgQIAAgVEFBMBRK6tfBAgQIECAAIFCQAAsYDQTIECAAAECBEYVEABHrax+ESBAgAABAgQKAQGwgNFMgAABAgQIEBhVQAActbL6RYAAAQIECBAoBATAAkYzAQIECBAgQGBUAQFw1MrqFwECBAgQIECgEBAACxjNBAgQIECAAIFRBQTAUSurXwQIECBAgACBQkAALGA0EyBAgAABAgRGFRAAR62sfhEgQIAAAQIECgEBsIDRTIAAAQIECBAYVUAAHLWy+kWAAAECBAgQKAQEwAJGMwECBAgQIEBgVAEBcNTK6hcBAgQIECBAoBAQAAsYzQQIECBAgACBUQUEwFErq18ECBAgQIAAgUJAACxgNBMgQIAAAQIERhUQAEetrH4RIECAAAECBAoBAbCA0UyAAAECBAgQGFVAABy1svpFgAABAgQIECgEBMACRjMBAgQIECBAYFQBAXDUyuoXAQIECBAgQKAQEAALGM0ECBAgQIAAgVEFBMBRK6tfBAgQIECAAIFCQAAsYDQTIECAAAECBEYVEABHrax+ESBAgAABAgQKAQGwgNFMgAABAgQIEBhVQAActbL6RYAAAQIECBAoBATAAkYzAQIECBAgQGBUAQFw1MrqFwECBAgQIECgEBAACxjNBAgQIECAAIFRBQTAUSurXwQIECBAgACBQkAALGA0EyBAgAABAgRGFRAAR62sfhEgQIAAAQIECgEBsIDRTIAAAQIECBAYVUAAHLWy+kWAAAECBAgQKAQEwAJGMwECBAgQIEBgVAEBcNTK6hcBAgQIECBAoBAQAAsYzQQIECBAgACBUQUEwFErq18ECBAgQIAAgUJAACxgNBMgQIAAAQIERhUQAEetrH4RIECAAAECBAoBAbCA0UyAAAECBAgQGFVAABy1svpFgAABAgQIECgEBMACRjMBAgQIECBAYFQBAXDUyuoXAQIECBAgQKAQEAALGM0ECBAgQIAAgVEFBMBRK6tfBAgQIECAAIFCQAAsYDQTIECAAAECBEYVEABHrax+ESBAgAABAgQKAQGwgNFMgAABAgQIEBhVQAActbL6RYAAAQIECBAoBATAAkYzAQIECBAgQGBUAQFw1MrqFwECBAgQIECgEBAACxjNBAgQIECAAIFRBQTAUSurXwQIECBAgACBQkAALGA0EyBAgAABAgRGFRAAR62sfhEgQIAAAQIECgEBsIDRTIAAAQIECBAYVUAAHLWy+kWAAAECBAgQKAQEwAJGMwECBAgQIEBgVAEBcNTK6hcBAgQIECBAoBAQAAsYzQQIECBAgACBUQUEwFErq18ECBAgQIAAgUJAACxgNBMgQIAAAQIERhUQAEetrH4RIECAAAECBAoBAbCA0UyAAAECBAgQGFVAABy1svpFgAABAgQIECgEBMACRjMBAgQIECBAYFQBAXDUyuoXAQIECBAgQKAQEAALGM0ECBAgQIAAgVEFBMBRK6tfBAgQIECAAIFCQAAsYDQTIECAAAECBEYVEABHrax+ESBAgAABAgQKAQGwgNFMgAABAgQIEBhVQAActbL6RYAAAQIECBAoBATAAkYzAQIECBAgQGBUAQFw1MrqFwECBAgQIECgEBAACxjNBAgQIECAAIFRBf4P5ZE/BEkeK48AAAAASUVORK5CYII=',
            reported: {},
            chartOptions: {
                title: {
                    text: null
                },
                series: [
                    {
                        name: 'Altitude',
                        data: []
                    },
                    {
                        name: 'Pitch',
                        data: []
                    },
                    {
                        name: 'Roll',
                        data: []
                    },
                    {
                        name: 'Yaw',
                        data: []
                    }
                ],
                plotOptions: {
                    line: {
                        marker: {
                            enabled: false
                        }
                    }
                }
            }

        };

        this.startStreaming = this.startStreaming.bind(this);
        this.stopStreaming = this.stopStreaming.bind(this);
        this.connectDrone = this.connectDrone.bind(this)
        this.disconnectDrone = this.disconnectDrone.bind(this);
        this.takeOff = this.takeOff.bind(this);
        this.land = this.land.bind(this);
        this.mission = this.mission.bind(this);
        this.subscribe = this.subscribe.bind(this);
        this.updateShadow = this.updateShadow.bind(this);

    }

    render() {

        const { chartOptions } = this.state;

        var gimbal_pitch_options = [
            {
                key: 'Forward',
                text: 'Forward (0.0)',
                value: 0.0
            },
            {
                key: 'Downward',
                text: 'Downward (-90.0)',
                value: -90.0
            }
        ]

        var gimbal_speed_options = [
            {
                key: 'Racing',
                text: 'Racing (45.0)',
                value: 45.0
            },
            {
                key: 'Sport',
                text: 'Sport (20.0)',
                value: 20.0
            }
        ]

        var max_tilt_options = [
            {
                key: 'Sport',
                text: 'Racing (25.0)',
                value: 25.0
            },
            {
                key: 'Cinematic',
                text: 'Cinematic (20.0)',
                value: 20.0
            },
            {
                key: 'Film',
                text: 'Film (10.0)',
                value: 10.0
            }
        ]

        var max_rotation_speed_options = [
            {
                key: 'Film',
                text: 'Film (10.0)',
                value: 10.0
            },
            {
                key: 'Sport',
                text: 'Sport (20.0)',
                value: 20.0
            },
            {
                key: 'Racing',
                text: 'Racing (40.0)',
                value: 40.0
            }
        ]

        var max_vertical_speed_options = [
            {
                key: 'Film',
                text: 'Film (1.0)',
                value: 1.0
            },
            {
                key: 'Sport',
                text: 'Sport (2.0)',
                value: 2.0
            },
            {
                key: 'Cinematic',
                text: 'Cinematic (2.5)',
                value: 2.5
            },
            {
                key: 'Racing',
                text: 'Racing (3.0)',
                value: 3.0
            }
        ]

        var flight_alt_options = [
            {
                key: 'Ceiling',
                text: 'Top (3.0)',
                value: 3.0
            },
            {
                key: 'Mid',
                text: 'Mid (2.0)',
                value: 2.0
            },
            {
                key: 'Floor',
                text: 'Film (1.0)',
                value: 1.0
            }
        ]

        var detection_enabled_options = [
            {
                key: 'True',
                text: 'True',
                value: true
            },
            {
                key: 'False',
                text: 'False',
                value: false
            }
        ]

        var detection_mode_options = [
            {
                key: 'Cars',
                text: 'Cars',
                value: 'cars'
            },
            {
                key: 'Drones',
                text: 'Drones',
                value: 'drones'
            }
        ]

        var car_detection_options = [
            {
                key: 'Porsche',
                text: 'Porsche (yellow)',
                value: 'porsche-yellow'
            },
            {
                key: 'Ferrari',
                text: 'Ferrari (red)',
                value: 'ferrari-red'
            },
            {
                key: 'Lamborghini-White',
                text: 'Lamborghini (white)',
                value: 'lamborghini-white'
            },
            {
                key: 'Lamborghini',
                text: 'Lamborghini (orange)',
                value: 'lamborghini-orange'
            }
        ]

        return (
            <div>
                <Segment>
                    <Grid columns={3} relaxed='very'>
                        <Grid.Column>

                            <Header as='h2' textAlign='center'>
                                <Header.Content>
                                    {this.state.thingName}
                                    <Header.Subheader>Parrot ANAFI drone</Header.Subheader>
                                </Header.Content>
                            </Header>

                            <img alt="feed" style={{ width: '640px', height: '360px' }} src={`data:image/jpeg;base64,${this.state.message}`} />
                            <Button.Group basic>
                                <Button onClick={this.connectDrone}>Connect</Button>
                                <Button onClick={this.startStreaming}>Start Streaming</Button>
                                <Button onClick={this.stopStreaming}>Stop Streaming</Button>
                                <Button onClick={this.disconnectDrone}>Disconnect</Button>
                            </Button.Group>
                            <Button.Group basic>
                                <Button onClick={this.takeOff}>Take Off</Button>
                                <Button onClick={this.land}>Land</Button>
                                <Button onClick={this.mission}>Mission</Button>
                            </Button.Group>
                        </Grid.Column>
                        <Grid.Column>

                            <Header as='h2' textAlign='center'>
                                <Header.Content>
                                    Shadow
                                <Header.Subheader>updated as state changes</Header.Subheader>
                                </Header.Content>
                            </Header>

                            <Statistic.Group widths='five' size='mini'>
                                <Statistic>
                                    <Statistic.Value>{this.state.reported.flying_state}</Statistic.Value>
                                    <Statistic.Label>Status</Statistic.Label>
                                </Statistic>

                                <Statistic>
                                    <Statistic.Value>{this.state.reported.alert_state}</Statistic.Value>
                                    <Statistic.Label>Alert</Statistic.Label>
                                </Statistic>

                                <Statistic>
                                    <Statistic.Value>{this.state.reported.motion_state}</Statistic.Value>
                                    <Statistic.Label>Motion</Statistic.Label>
                                </Statistic>

                                <Statistic>
                                    <Statistic.Value>{this.state.reported.wind_state}</Statistic.Value>
                                    <Statistic.Label>Wind</Statistic.Label>
                                </Statistic>

                                <Statistic>
                                    <Statistic.Value>{this.state.reported.vibration_level}</Statistic.Value>
                                    <Statistic.Label>Vibration Level</Statistic.Label>
                                </Statistic>

                            </Statistic.Group>

                            <Table compact>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell>Attribute</Table.HeaderCell>
                                        <Table.HeaderCell>Units</Table.HeaderCell>
                                        <Table.HeaderCell>Reported</Table.HeaderCell>
                                        <Table.HeaderCell>Desired</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>

                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>Max Altitude</Table.Cell>
                                        <Table.Cell>meters</Table.Cell>
                                        <Table.Cell>{this.state.reported.max_alt}</Table.Cell>
                                        <Table.Cell><Icon name='lock' /></Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Max Vertical Speed</Table.Cell>
                                        <Table.Cell>meters/second</Table.Cell>
                                        <Table.Cell>{this.state.reported.max_vertical_speed}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='max_vertical_speed'
                                                fluid
                                                selection
                                                options={max_vertical_speed_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Max Rotation Speed</Table.Cell>
                                        <Table.Cell>degrees/second</Table.Cell>
                                        <Table.Cell>{this.state.reported.max_rotation_speed}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='max_rotation_speed'
                                                fluid
                                                selection
                                                options={max_rotation_speed_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Max Tilt</Table.Cell>
                                        <Table.Cell>degrees</Table.Cell>
                                        <Table.Cell>{this.state.reported.max_tilt}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='max_tilt'
                                                fluid
                                                selection
                                                options={max_tilt_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Gimbal Pitch</Table.Cell>
                                        <Table.Cell>degrees</Table.Cell>
                                        <Table.Cell>{this.state.reported.gimbal_pitch}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='gimbal_pitch'
                                                fluid
                                                selection
                                                options={gimbal_pitch_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Gimbal Speed</Table.Cell>
                                        <Table.Cell>degrees</Table.Cell>
                                        <Table.Cell>{this.state.reported.gimbal_speed}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='gimbal_speed'
                                                fluid
                                                selection
                                                options={gimbal_speed_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Takeoff Altitude</Table.Cell>
                                        <Table.Cell>meters</Table.Cell>
                                        <Table.Cell>{this.state.reported.flight_altitude}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='flight_altitude'
                                                fluid
                                                selection
                                                options={flight_alt_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Detection Enabled</Table.Cell>
                                        <Table.Cell>-</Table.Cell>
                                        <Table.Cell>{`${this.state.reported.detection_enabled}`}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='detection_enabled'
                                                fluid
                                                selection
                                                options={detection_enabled_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Detection Mode</Table.Cell>
                                        <Table.Cell>-</Table.Cell>
                                        <Table.Cell>{this.state.reported.detection_mode}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='detection_mode'
                                                fluid
                                                selection
                                                options={detection_mode_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Targeted Car</Table.Cell>
                                        <Table.Cell>-</Table.Cell>
                                        <Table.Cell>{this.state.reported.targeted_car}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                placeholder='targeted_car'
                                                fluid
                                                selection
                                                options={car_detection_options}
                                                onChange={this.updateShadow}
                                            />
                                        </Table.Cell>
                                    </Table.Row>
                                </Table.Body>
                            </Table>

                        </Grid.Column>
                        <Grid.Column>
                            {/* <Button.Group basic>
                                <Button onClick={this.updateSeries}>Update Chart</Button>
                                <Button onClick={this.resetCharts}>Reset Chart</Button>
                            </Button.Group> */}

                            <Header as='h2' textAlign='center'>
                                <Header.Content>
                                    Telemetry
                                <Header.Subheader>published every second</Header.Subheader>
                                </Header.Content>
                            </Header>

                            <HighchartsReact
                                highcharts={Highcharts}
                                options={chartOptions}
                            />
                            <Statistic size='mini'>
                                <Statistic.Label>Altitude (m)</Statistic.Label>
                                <Statistic.Value>{this.state.telemetry.altitude}</Statistic.Value>
                            </Statistic>

                            <Statistic size='mini'>
                                <Statistic.Label>Pitch</Statistic.Label>
                                <Statistic.Value>{this.state.telemetry.pitch}</Statistic.Value>
                            </Statistic>

                            <Statistic size='mini'>
                                <Statistic.Label>Roll</Statistic.Label>
                                <Statistic.Value>{this.state.telemetry.roll}</Statistic.Value>
                            </Statistic>

                            <Statistic size='mini'>
                                <Statistic.Label>Yaw</Statistic.Label>
                                <Statistic.Value>{this.state.telemetry.yaw}</Statistic.Value>
                            </Statistic>

                        </Grid.Column>
                    </Grid>
                </Segment>
            </div>
        );
    }

    async connectDrone() {
        await PubSub.publish(`commands/${this.state.thingName}`, { command: 'connect' });
    }

    async disconnectDrone() {
        await PubSub.publish(`commands/${this.state.thingName}`, { command: 'disconnect' });
    }

    async startStreaming() {
        await PubSub.publish(`commands/${this.state.thingName}`, { command: 'start-streaming' });
    }

    async stopStreaming() {
        await PubSub.publish(`commands/${this.state.thingName}`, { command: 'stop-streaming' });
    }

    async takeOff() {
        await PubSub.publish(`commands/${this.state.thingName}`, { command: 'take-off' });
    }

    async land() {
        await PubSub.publish(`commands/${this.state.thingName}`, { command: 'land' });
    }

    async mission() {
        await PubSub.publish(`commands/${this.state.thingName}`, { command: 'mission' });
    } x

    async updateShadow(e, data) {
        console.log(data.placeholder);
        console.log(data.value);

        var payload = { state: { desired: {} } };
        payload.state.desired[data.placeholder] = data.value;

        await PubSub.publish(`$aws/things/${this.state.thingName}/shadow/update`, payload);
    }

    updateSeries = (telemetryRecord) => {

        var currentData = this.state.chartOptions.series
        currentData[0].data.push(telemetryRecord.value.altitude);
        currentData[1].data.push(telemetryRecord.value.pitch);
        currentData[2].data.push(telemetryRecord.value.roll);
        currentData[3].data.push(telemetryRecord.value.yaw);

        // The chart is updated only with new options.
        this.setState({
            chartOptions: {
                series: currentData
            }
        });
    }

    resetCharts = () => {

        // The chart is updated only with new options.
        this.setState({
            chartOptions: {
                series: [
                    {
                        name: 'Altitude',
                        data: []
                    },
                    {
                        name: 'Pitch',
                        data: []
                    },
                    {
                        name: 'Roll',
                        data: []
                    },
                    {
                        name: 'Yaw',
                        data: []
                    }
                ]
            }
        });
    }

    subscribe() {

        var framesSub = PubSub.subscribe(`${this.state.thingName}/frames`).subscribe({
            next: data => {
                this.setState({ message: data.value.b64, last_timestamp: data.value.timestamp });
            },
            error: error => console.error(error),
            close: () => console.log('Done'),
        });
        subscriptions.push(framesSub);

        var predictionCarsSub = PubSub.subscribe(`detections/${this.state.thingName}/infer/output`).subscribe({
            next: data => {
                this.setState({ message: data.value.b64, last_timestamp: data.value.timestamp });
                // console.log('Image received', data)
            },
            error: error => console.error(error),
            close: () => console.log('Done'),
        });
        subscriptions.push(predictionCarsSub);

        var predictionDronesSub = PubSub.subscribe(`detections/${this.state.thingName}/infer/output`).subscribe({
            next: data => {
                this.setState({ message: data.value.b64, last_timestamp: data.value.timestamp });
                // console.log('Image received', data)
            },
            error: error => console.error(error),
            close: () => console.log('Done'),
        });
        subscriptions.push(predictionDronesSub);

        var commandsSub = PubSub.subscribe(`commands/${this.state.thingName}/ack`).subscribe({
            next: data => {
                // console.log('ACK received', data)

                var toastType = 'error'

                if (data.value.success && data.value.success === true) {
                    toastType = 'success'
                }

                setTimeout(() => {
                    toast(
                        {
                            type: toastType,
                            title: 'Command ACK',
                            description: <p>{this.state.thingName} - {data.value.command}</p>
                        }
                    );
                }, 500);
            },
            error: error => console.error(error),
            close: () => console.log('Done'),
        });
        subscriptions.push(commandsSub);

        var droneTelemetrySub = PubSub.subscribe(this.state.thingName).subscribe({
            next: data => {

                this.updateSeries(data);

                data.value.altitude = data.value.altitude.toFixed(3)
                data.value.pitch = data.value.pitch.toFixed(3)
                data.value.roll = data.value.roll.toFixed(3)
                data.value.yaw = data.value.yaw.toFixed(3)

                this.setState({ telemetry: data.value });
                // console.log('Message received', data)
            },
            error: error => console.error(error),
            close: () => console.log('Done'),
        });
        subscriptions.push(droneTelemetrySub);

        var droneShadowSub = PubSub.subscribe(`$aws/things/${this.state.thingName}/shadow/get/accepted`).subscribe({
            next: data => {

                console.log('Message received', data)

                if (data.value.state.reported) {
                    this.setState({ reported: data.value.state.reported });
                }
            },
            error: error => console.error(error),
            close: () => console.log('Done'),
        });
        subscriptions.push(droneShadowSub);

        var droneShadowDeltaSub = PubSub.subscribe(`$aws/things/${this.state.thingName}/shadow/update/accepted`).subscribe({
            next: data => {
                // this.setState({ telemetry: data.value });
                if (data.value.state.reported) {

                    if (data.value.state.reported.gimbal_pitch) {
                        data.value.state.reported.gimbal_pitch = data.value.state.reported.gimbal_pitch.toFixed(1)
                    }

                    if (data.value.state.reported.gimbal_speed) {
                        data.value.state.reported.gimbal_speed = data.value.state.reported.gimbal_speed.toFixed(1)
                    }

                    if (data.value.state.reported.max_tilt) {
                        data.value.state.reported.max_tilt = data.value.state.reported.max_tilt.toFixed(1)
                    }

                    this.setState({ reported: data.value.state.reported });
                }

                console.log('Shadow update received', data)
            },
            error: error => console.error(error),
            close: () => console.log('Done'),
        });
        subscriptions.push(droneShadowDeltaSub);

    }

    unsubscribe() {
        subscriptions.forEach(function (sub) {
            if (sub !== null) {
                sub.unsubscribe();
            }
        });
    }

    componentDidMount() {
        Auth.currentCredentials().then((info) => {
            console.log(info);
            const cognitoIdentityId = info.data.IdentityId;
            console.log(cognitoIdentityId);

            const iot = new IoT({
                apiVersion: '2015-05-28',
                credentials: Auth.essentialCredentials(info),
                region: Config.region
            });
            var params = {
                policyName: `${this.state.thingName}${Config.iot_policy_suffix}`,
                principal: cognitoIdentityId
            };
            iot.attachPrincipalPolicy(params, function (err, data) {
                if (err) console.log(err, err.stack);
            });
        });
        this.subscribe();

        setTimeout(() => {
            PubSub.publish(`$aws/things/${this.state.thingName}/shadow/get`, {});
        }, 2000);
    }

    componentWillUnmount() {
        this.unsubscribe();
    }
}

export default Dashboard;