/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Performance optimizations
  compress: true, // Enable gzip compression

  // Enable Turbopack for faster compilation (Next.js 16+)
  // Turbopack is now the default bundler in Next.js 16

  // Optimize images
  images: {
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
  },

  // Reduce memory usage during builds
  experimental: {
    // Optimize package imports for faster builds
    optimizePackageImports: ['lucide-react', 'zustand'],
  },

  // Enable static optimization
  poweredByHeader: false, // Remove X-Powered-By header for security
}

module.exports = nextConfig
