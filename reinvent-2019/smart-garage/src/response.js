const uuid = require('uuid');

class AlexaResponse {
    constructor(opts) {
      this.context = {properties: []};
      this.event = {
          header: {
            namespace: this.checkValue(opts.namespace, "Alexa"),
            name: this.checkValue(opts.name, "Response"),
            messageId: this.checkValue(opts.messageId, uuid()),
            correlationToken: this.checkValue(opts.correlationToken, undefined),
            payloadVersion: this.checkValue(opts.payloadVersion, "3")
          },
          endpoint: {
              scope: {
                type: "BearerToken",
                token: this.checkValue(opts.token, "INVALID"),
              },
              endpointId: this.checkValue(opts.endpointId, "INVALID")
          },
          payload: this.checkValue(opts.payload, {})
      };

      if (opts.context)
          this.context = this.checkValue(opts.context, this.context);

      if (opts.event)
          this.event = this.checkValue(opts.event, this.event);

      // No endpoint in an AcceptGrant or Discover request
      const headerName = this.event.header.name.toLowerCase();
      if (headerName === "acceptgrant.response" || headerName === "discover.response")
          delete this.event.endpoint;
    }

    addContextProperty(opts) {
      this.context.properties.push(this.createContextProperty(opts));
    }

    addPayloadEndpoint(opts) {
      this.event.payload.endpoints = this.event.payload.endpoints || [];
      this.event.payload.endpoints.push(this.createPayloadEndpoint(opts));
    }

    createContextProperty(opts) {
      return {
          namespace: this.checkValue(opts.namespace, "Alexa.EndpointHealth"),
          name: this.checkValue(opts.name, "connectivity"),
          value: this.checkValue(opts.value, {value: "OK"}), // UNREACHABLE
          timeOfSample: new Date().toISOString(),
          uncertaintyInMilliseconds: this.checkValue(opts.uncertaintyInMilliseconds, 0)
      };
    }

    createPayloadEndpoint(opts) {
      if (opts === undefined) opts = {};

      const endpoint = {
        capabilities: this.checkValue(opts.capabilities, []),
        description: this.checkValue(opts.description, "To open / close garage"),
        displayCategories: this.checkValue(opts.displayCategories, ["SMARTLOCK"]),
        endpointId: this.checkValue(opts.endpointId, 'endpoint-001'),
        // "endpointId": this.checkValue(opts.endpointId, 'endpoint_' + (Math.floor(Math.random() * 90000) + 10000)),
        friendlyName: this.checkValue(opts.friendlyName, "Garage"),
        manufacturerName: this.checkValue(opts.manufacturerName, "Smart Garage INC")
      };

      if (opts.hasOwnProperty("cookie"))
        endpoint["cookie"] = this.checkValue('cookie', {});

      return endpoint
    }

    /**
     * Creates a capability for an endpoint within the payload.
     * @param opts Contains options for the endpoint capability.
     */
    createPayloadEndpointCapability(opts) {
        if (opts === undefined) opts = {};

        let capability = {};
        capability['type'] = this.checkValue(opts.type, "AlexaInterface");
        capability['interface'] = this.checkValue(opts.interface, "Alexa");
        capability['version'] = this.checkValue(opts.version, "3");
        let supported = this.checkValue(opts.supported, false);
        if (supported) {
            capability['properties'] = {};
            capability['properties']['supported'] = supported;
            capability['properties']['proactivelyReported'] = this.checkValue(opts.proactivelyReported, false);
            capability['properties']['retrievable'] = this.checkValue(opts.retrievable, false);
        }
        return capability
    }

    /**
     * Get the composed Alexa Response.
     * @returns {AlexaResponse}
     */
    get() {
        return this;
    }

    checkValue(value, defaultValue) {
      if (value === undefined || value === {} || value === "")
        return defaultValue;

      return value;
    }
}

module.exports = AlexaResponse;
