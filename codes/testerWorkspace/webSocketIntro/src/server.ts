import * as express from 'express';
import * as http from 'http';
import * as WebSocket from 'ws';

const app = express();

// Initialize a simpel http server
const server = http.createServer(app);

// Initialize the wbesocket server instance
const wss = new WebSocket.Server({server});

wss.on('connection', (ws: WebSocket) =>{
    // establish a connection 
    // Add simple event to test 
})