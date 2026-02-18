# CUE WEBAPP DEFENSE STRATEGY
**Date:** 2026-01-30
**Status:** IMMEDIATE ACTION REQUIRED

## 1. URGENT PATCH: RATE LIMITING (DoS PREVENTION)
The current lack of rate limiting on `/api/health`, `/login`, and `/signup` leaves the platform vulnerable to resource exhaustion.

### Recommended Fix (Next.js Middleware)
Implement `upstash/ratelimit` or a custom Redis-backed middleware to cap requests.

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"), // 10 requests per 10 seconds
});

export async function middleware(request: NextRequest) {
  const ip = request.ip ?? '127.0.0.1';
  
  // Apply only to sensitive routes
  if (request.nextUrl.pathname.startsWith('/api/health') || 
      request.nextUrl.pathname.startsWith('/login')) {
      
    const { success } = await ratelimit.limit(ip);
    
    if (!success) {
      return new NextResponse('Too Many Requests', { status: 429 });
    }
  }
  return NextResponse.next();
}
```

## 2. SECURING THE STRIPE ENDPOINT
The `/api/v2/stripe` endpoint is accepting unauthenticated POST requests. This allows for "Plan Injection."

### Fix: Verify Stripe Signatures
You must verify that the request actually came from Stripe using their official SDK.

```javascript
// pages/api/v2/stripe.js
import { buffer } from 'micro';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

export const config = {
  api: {
    bodyParser: false, // Disallow default parsing, we need the raw buffer
  },
};

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const buf = await buffer(req);
    const sig = req.headers['stripe-signature'];

    let event;

    try {
      // CRITICAL: This line prevents fake payloads
      event = stripe.webhooks.constructEvent(buf, sig, webhookSecret);
    } catch (err) {
      return res.status(400).send(`Webhook Error: ${err.message}`);
    }

    // Handle the event securely...
    res.status(200).json({ received: true });
  }
}
```

## 3. INFRASTRUCTURE HARDENING
1.  **Cloudflare Rules:** Enable "Under Attack Mode" or set a WAF rule to block requests to `/api/*` that do not contain a valid `Referer` or `Authorization` header.
2.  **Disable Source Maps:** Ensure `production` builds do not emit `.map` files, which help attackers reverse-engineer your code.
3.  **Audit Logs:** Log all failed login attempts and 401/403 errors on the Stripe endpoint to detect probing.
