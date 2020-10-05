// Creating map object

var dropDownList1 = d3.select("#selDataset1");
var dropDownList2 = d3.select("#selDataset2");
var dropDownList3 = d3.select("#selDataset3");


url = "http://127.0.0.1:5000/product/product_list"

function init() {
    d3.json(url).then(function(data) {
        var product = []
        data.forEach(function(item) {
            product.push(item.product_name);
        });

        console.log(product)

        var options = dropDownList1.selectAll("option")
            .data(product)
            .enter()
            .append("option")
            .text(function(d) { return d })
            .attr("value", function(d) { return d });

        var options2 = dropDownList2.selectAll("option")
            .data(product)
            .enter()
            .append("option")
            .text(function(d) { return d })
            .attr("value", function(d) { return d });

        var options3 = dropDownList3.selectAll("option")
            .data(product)
            .enter()
            .append("option")
            .text(function(d) { return d })
            .attr("value", function(d) { return d });


    });
};

d3.selectAll("#buy").on("click", updateProduct);

function updateProduct() {
    var dropDownList1 = d3.select("#selDataset1");
    var dropDownList2 = d3.select("#selDataset2");
    var dropDownList3 = d3.select("#selDataset3");

    item1 = dropDownList1.property("value");
    item2 = dropDownList2.property("value");
    item3 = dropDownList3.property("value");


    url2 = "http://127.0.0.1:5000/shop/" + item1 + "/" + item2 + "/" + item3;

    d3.json(url2, function(error, result) {

        var infoPanel = d3.select("#nextproduct");
        infoPanel.html("")
        infoPanel.append("h5").text(`${result.product}, <\br> Find it in Department: ${result.department} in Aisle: ${result.aisle}`)
    });
};


init()