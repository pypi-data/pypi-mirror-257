// Copyright (c) 2024 iiPython

// Main server class
class NightwatchServer {
    constructor(address) {
        address = address.split(":");

        this.host = address[0];
        this.port = address[1] ? Number(address[1]) : 443;

        // Connect socket
        this._callbacks = {};
        this.connect();
    }

    connect() {
        if (this._interval) clearInterval(this._interval);
        this.socket = new WebSocket(`${this.port == 443 ? 'wss' : 'ws'}://${this.host}:${this.port}/gateway`);
        this.socket.addEventListener("message", (d) => {
            const data = JSON.parse(d.data);
            const callback = this._callbacks[data.callback];
            if (callback) {
                delete this._callbacks[data.callback];
                return callback(data);
            }
            if (data.type == "message" && this._onmessage) this._onmessage(data);
        });
        this.socket.addEventListener("open", () => { if (this._connected) this._connected(); });
        this._interval = setInterval(() => { this.send_payload("ping"); }, 10000);
    }

    connected(callback) {
        this._connected = callback;
    }

    on_message(callback) {
        this._onmessage = callback;
    }

    send_payload(type, data, callback) {
        if (!this.socket) throw new Error("Current Nightwatch websocket is not connected!");
        let payload = { data: data };
        if (callback) {
            let callback_id = nanoid();
            payload.callback = callback_id;
            this._callbacks[callback_id] = callback;
        }
        this.socket.send(JSON.stringify({ type: type, ...payload }));
    }

    close() {
        this.socket.close();
    }

    // Main events
    identify(username, color, callback) {
        this.user = { name: username, color: color };
        this.send_payload("identify", this.user, callback);
    }

    message(content) {
        this.send_payload("message", { text: content });
    }
}
