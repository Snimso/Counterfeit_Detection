const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

// Updated MongoDB connection string with database name
mongoose
  .connect(
    "mongodb+srv://priyanshushekhar100:L0YxKHq2WYJHBkvg@cluster0.kfc1wq1.mongodb.net/amazon?authMechanism=SCRAM-SHA-1"
  )
  .then(() => console.log("MongoDB connection successful"))
  .catch((err) => console.error("MongoDB connection error:", err));

// Schema definition
const productSchema = new mongoose.Schema({
  Product_link: String,
  Photo_url: String,
  Description: String,
  Unique_product_id: String,
  Price: Number,
  Product_score: Number,
  review_bold: String,
  ratings: Number,
  review: String,
  verified: Boolean,
  date: String,
  by: String,
  helpful: Number,
  FINAL_SCORE: Number,
});

// Explicitly specifying the collection name
const Product = mongoose.model("Product", productSchema, "amazon");

// Route to get products
app.get('/products/:Unique_product_id', async (req, res) => {
  try {
    const uniqueId = req.params.Unique_product_id;
    
    const products = await Product.find({ Unique_product_id });

    if (products.length === 0) {
      return res.status(404).json({ message: 'No products found with the given ID.' });
    }

    res.json(products);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});


app.get('/products/:uniqueId', async (req, res) => {
  try {
    const uniqueId = req.params.uniqueId;
    const product = await Product.findOne({ Unique_product_id: uniqueId });
    if (!product) {
      return res.status(404).send('Product not found');
    }
    res.json(product);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
