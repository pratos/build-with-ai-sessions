/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

import { Container } from "@cloudflare/containers";

export class StreamlitContainer extends Container {
	// Port the container listens on (Streamlit default: 8080)
	defaultPort = 8080;
	// Time before container sleeps due to inactivity 
	sleepAfter = "10m"; // Longer timeout for interactive apps
	// Environment variables passed to the container
	envVars = {
		ENVIRONMENT: "production",
		STREAMLIT_SERVER_PORT: "8080",
		STREAMLIT_SERVER_ADDRESS: "0.0.0.0",
		STREAMLIT_SERVER_HEADLESS: "true",
		STREAMLIT_BROWSER_GATHER_USAGE_STATS: "false",
		STREAMLIT_SERVER_ENABLE_CORS: "true",
	};

	// Optional lifecycle hooks
	override onStart() {
		console.log("Streamlit container successfully started");
	}

	override onStop() {
		console.log("Streamlit container successfully shut down");
	}

	override onError(error: unknown) {
		console.log("Streamlit container error:", error);
	}
}

export interface Env {
	MY_CONTAINER: DurableObjectNamespace<StreamlitContainer>;
	ENVIRONMENT: string;
}

export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
		const url = new URL(request.url);
		
		// Health check endpoint
		if (url.pathname === '/health') {
			return new Response('OK', { status: 200 });
		}

		// Get or create a singleton Streamlit container
		const containerId = env.MY_CONTAINER.idFromName("streamlit-app");
		const container = env.MY_CONTAINER.get(containerId);
		
		try {
			// Proxy the request to the Streamlit container
			const response = await container.fetch(request);
			
			// Add security headers
			const newResponse = new Response(response.body, response);
			newResponse.headers.set('X-Frame-Options', 'SAMEORIGIN');
			newResponse.headers.set('X-Content-Type-Options', 'nosniff');
			newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
			
			return newResponse;
		} catch (error) {
			console.error("Error proxying to Streamlit container:", error);
			
			// Return a helpful error page if the container fails
			const errorHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCPs + Agents Demo - Starting Up</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            padding: 3rem;
            max-width: 500px;
            text-align: center;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 2rem;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        h1 { color: #333; margin-bottom: 1rem; }
        p { color: #666; line-height: 1.6; }
        .retry { 
            background: #007bff; 
            color: white; 
            padding: 0.75rem 1.5rem; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            margin-top: 1rem;
            text-decoration: none;
            display: inline-block;
        }
        .retry:hover { background: #0056b3; }
    </style>
    <script>
        // Auto-refresh every 10 seconds
        setTimeout(() => window.location.reload(), 10000);
    </script>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>🤖 Starting MCPs + Agents Demo</h1>
        <p>
            Your Streamlit container is starting up. This may take 30-60 seconds on first load.
            <br><br>
            The page will automatically refresh in 10 seconds.
        </p>
        <a href="/" class="retry">Refresh Now</a>
    </div>
</body>
</html>
			`;
			
			return new Response(errorHtml, {
				status: 503,
				headers: {
					'Content-Type': 'text/html',
					'Retry-After': '10',
				},
			});
		}
	},
};
