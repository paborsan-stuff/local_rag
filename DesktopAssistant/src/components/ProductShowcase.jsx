import React from 'react'

const products = [
  { id: 1, title: "Feature One" },
  { id: 2, title: "Feature Two" },
  { id: 3, title: "Feature Three" },
  { id: 4, title: "Feature Four" },
  { id: 5, title: "Feature Five" },
  { id: 6, title: "Feature Six" },
]

function ProductShowcase() {
  return (
    <section className="py-12 bg-gray-100" style={{ backgroundColor: '#212121' }}>
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-8">Our Features</h2>
        <div className="grid grid-cols-3 gap-6">
          {products.map(product => (
            <div key={product.id} className="p-4 rounded-lg shadow">
              <div className="w-full h-40 bg-gray-300 mb-4 flex items-center justify-center">
                <span>Image</span>
              </div>
              <h3 className="text-xl font-medium text-center">{product.title}</h3>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default ProductShowcase
