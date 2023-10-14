import './App.css'
import Home from "./pages/home/components/Home";
import {Route, Routes} from "react-router-dom";
import ComparisonCity from "./modules/comparison/components/СomparisonCity";
import ComparisonArea from "./modules/comparison/components/СomparisonArea";

function App() {

  return (
    <div className="wrapper">
      <Routes>
        <Route path="/" element={<Home/>}></Route>
        <Route path="/comparisonCity" element={<ComparisonCity/>}></Route>
        <Route path="/comparisonArea" element={<ComparisonArea/>}></Route>
      </Routes>
    </div>
  )
}

export default App
