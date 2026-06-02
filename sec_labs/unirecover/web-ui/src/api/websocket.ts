// WebSocket broker for live job progress
export const connectProgressStream = (onMessage: (data: any) => void) => {
    const ws = new WebSocket('ws://127.0.0.1:8080/api/v1/pipeline/progress');
    ws.onmessage = (event) => onMessage(JSON.parse(event.data));
    return ws;
};
