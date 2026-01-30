const express = require('express');
const path = require('path');
const localtunnel = require('localtunnel');

const app = express();
const PORT = 3000;

// Serve static files
app.use(express.static(path.join(__dirname)));

// Serve index.html for root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
const server = app.listen(PORT, async () => {
    console.log(`\n🎮 Game server running at:`);
    console.log(`   Local: http://localhost:${PORT}`);

    // Create localtunnel for mobile access
    try {
        const tunnel = await localtunnel({ port: PORT });
        console.log(`   Mobile: ${tunnel.url}`);
        console.log(`\n📱 Scan QR code or open the Mobile URL on your phone!`);
        console.log(`\n   Press Ctrl+C to stop the server.\n`);

        tunnel.on('close', () => {
            console.log('Tunnel closed');
        });

        tunnel.on('error', (err) => {
            console.log('Tunnel error:', err.message);
        });
    } catch (err) {
        console.log(`   Mobile: (localtunnel failed: ${err.message})`);
        console.log(`   Try using ngrok or your local IP instead.`);
    }
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n\n👋 Shutting down server...');
    server.close(() => {
        console.log('Server closed.');
        process.exit(0);
    });
});
