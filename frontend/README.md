# Frontend

Using [AI chatbot app](https://github.com/vercel/ai-chatbot) as a template

## Run locally

```sh
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm install
npm run dev
```

## Build and Run

```sh
echo "NEXT_PUBLIC_API_URL=${BACKEND_API_URL}" > .env.local

npm install

./node_modules/.bin/next build
./node_modules/.bin/next start
```
