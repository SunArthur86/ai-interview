import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  basePath: process.env.NODE_ENV === 'production' ? '/interview-ai' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/interview-ai/' : undefined,
  trailingSlash: true,
  images: { unoptimized: true },
};

export default nextConfig;
