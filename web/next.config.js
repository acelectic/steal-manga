/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    reactStrictMode: true,
    experimental: {
        appDir: true,
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
        test: 'hello'
    }
}

module.exports = nextConfig
