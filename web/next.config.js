/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    reactStrictMode: true,
    experimental: {
        appDir: true,
        serverActions: true
    },
    async redirects() {
        return [
            {
                source: '/',
                destination: '/home', // Matched parameters can be used in the destination
                permanent: true,
            },
        ]
    },
    publicRuntimeConfig: {
        NEXT_PUBLIC_LOG_ROCKET_APP_ID: process.env.NEXT_PUBLIC_LOG_ROCKET_APP_ID,
        test: 'hello',
        KOYEB_API_HOST: process.env.KOYEB_API_HOST,
        KOYEB_API_SERVICE_ID: process.env.KOYEB_API_SERVICE_ID,
        KOYEB_API_KEY: process.env.KOYEB_API_KEY,
    }
}

module.exports = nextConfig
