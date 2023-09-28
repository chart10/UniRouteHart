echo "Building front-end bundle..."
export NODE_OPTIONS=--openssl-legacy-provider
npm run build
rm -rf api/static
rm -rf api/templates
mkdir api/templates
mv -v build/index.html api/templates/index.html
mv -fv build/static api/static
echo "Deploying to Fly.io..."
fly deploy