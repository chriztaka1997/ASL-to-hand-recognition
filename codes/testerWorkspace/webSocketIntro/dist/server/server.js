"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express = require("express");
const http = require("http");
const WebSocket = require("ws");
const app = express();
// Initialize a simpel http server
const server = http.createServer(app);
// Initialize the wbesocket server instance
const wss = new WebSocket.Server({ server });
wss.on('connection', (ws) => {
    // establish a connection 
    // Add simple event to test 
    ws.on('message', (message) => {
        // log the console file and send it back to client
        console.log('receive: %s', message);
        const broadcastRegex = /^broadcast\:/;
        if (broadcastRegex.test(message)) {
            message = message.replace(broadcastRegex, '');
            //send back the message to other clients
            wss.clients.forEach(client => {
                if (client != ws) {
                    client.send('Hello, broadcast message -> ${message}');
                }
            });
        }
        else {
            ws.send('Hello, you sent -> ${message}');
        }
    });
    ws.send('Hi there, I am a WebSocket');
});
// Start server
server.listen(3000, () => {
    console.log(`Server started on port 3000`);
});
//# sourceMappingURL=server.js.map