<template>
  <div class="graph-container" :id="randomid">
    <svg
      id="save-img-svg"
      :style="{ height: height + 'px', width: width + 'px' }"
    >
      <g id="save-img-svg-g"></g>
    </svg>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "DrawGraph",
  props: {
    filename: {
      type: String,
      default: "100.json",
    },
    width: {
      type: Number,
      default: 1300,
    },
    height: {
      type: Number,
      default: 600,
    },
  },
  data() {
    return {
      randomid: "save-img" + Math.random().toString(36).slice(-8),
      innerUrl: "http://10.9.21.98:13333/media/",
    };
  },
  mounted() {
    this.innerUrl += this.filename;
    var fontScale; //字体比例车
    var nodeScale; //节点比例车
    var linkScale; //边的比例尺
    var width = this.width, // svg width
      height = this.height,
      off = 5, // cluster hull offset/cluster 群，组 hull 壳
      collapse = {}, // collapsed clusters    收拢的群
      data,
      net,
      force,
      hullG,
      hull,
      linkG,
      link,
      nodeG,
      node;
    var save_img = d3.select("#" + this.randomid);
    var svg = save_img.select("#save-img-svg");
    var vis = save_img
      .select("#save-img-svg-g")
      // var svg = d3.select("#save-img-svg");
      // var vis = d3.select("#save-img-svg-g")
      .attr("cursor", "grab"); //选中节点时光标变成小手

    const curve = d3.svg.line().interpolate("cardinal-closed").tension(0.85);

    //生成了20种颜色用来填充
    const fill = d3.scale.category20();

    function nodeId(n) {
      return n.size ? "_g_" + n.group : n.name;
    }

    function linkId(l) {
      var u = nodeId(l.source),
        v = nodeId(l.target);
      return u < v ? u + "|" + v : v + "|" + u;
    }

    function getNode(nodes, name) {
      for (let i = 0; i < nodes.length; i++) {
        // console.log(nodes);
        if (name === nodes[i].name) return i;
      }
    }

    function getGroup(n) {
      return n.group;
    }

    // constructs the network to visualize
    function network(data, prev, index, collapse) {
      let i;
      let l;
      let k;
      collapse = collapse || {};
      var gm = {}, // group map
        nm = {}, // node map
        lm = {}, // link map
        gn = {}, // previous group nodes
        gc = {}, // previous group centroids //centroids 质心
        nodes = [], // output nodes
        links = []; // output links

      // process previous nodes for reuse or centroid calculation
      if (prev) {
        prev.nodes.forEach(function (n) {
          var i = index(n),
            o;
          if (n.size > 0) {
            gn[i] = n;
            n.size = 0;
          } else {
            o = gc[i] || (gc[i] = { x: 0, y: 0, count: 0 });
            o.x += n.x;
            o.y += n.y;
            o.count += 1;
          }
        });
      }

      // determine nodes
      for (k = 0; k < data.nodes.length; ++k) {
        let n = data.nodes[k];
        i = index(n);
        l =
          gm[i] ||
          (gm[i] = gn[i]) ||
          (gm[i] = { label: n.group, group: i, size: 0, nodes: [] });

        if (collapse[i] !== true) {
          // the node should be directly visible
          nm[n.name] = nodes.length;
          nodes.push(n);
          if (gn[i]) {
            // place new nodes at cluster location (plus jitter)
            n.x = gn[i].x + Math.random();
            n.y = gn[i].y + Math.random();
          }
        } else {
          // the node is part of a collapsed cluster
          if (l.size === 0) {
            // if new cluster, add to set and position at centroid of leaf nodes
            nm[i] = nodes.length;
            nodes.push(l);
            if (gc[i]) {
              l.x = gc[i].x / gc[i].count;
              l.y = gc[i].y / gc[i].count;
            }
          }
          l.nodes.push(n);
        }
        // always count group size as we also use it to tweak the force graph strengths/distances
        // l.size += n.times;
        l.size += nodeScale(n.times);
        n.group_data = l;
      }

      for (i in gm) {
        gm[i].link_count = 0;
      }
      // determine links
      for (k = 0; k < data.links.length; ++k) {
        var e = data.links[k],
          u = index(e.source),
          v = index(e.target);
        if (u !== v) {
          gm[u].link_count++;
          gm[v].link_count++;
        }
        u = !collapse[u] ? nm[e.source.name] : nm[u];
        v = !collapse[v] ? nm[e.target.name] : nm[v];
        i = u < v ? u + "|" + v : v + "|" + u;
        l = lm[i] || (lm[i] = { source: u, target: v, size: 0 });
        //这里可以控制连线的属性
        // l.size += 1;
        l.size = e.times;
        l.id = e.label;
      }
      for (i in lm) {
        links.push(lm[i]);
      }
      return { nodes: nodes, links: links };
    }

    function convexHulls(nodes, index, offset) {
      var hulls = {};

      // create point sets
      for (var k = 0; k < nodes.length; ++k) {
        var n = nodes[k];
        if (n.size) continue;
        var i = index(n),
          l = hulls[i] || (hulls[i] = []);
        l.push([n.x - offset, n.y - offset]);
        l.push([n.x - offset, n.y + offset]);
        l.push([n.x + offset, n.y - offset]);
        l.push([n.x + offset, n.y + offset]);
      }

      // create convex hulls
      var hullset = [];
      for (i in hulls) {
        hullset.push({ group: i, path: d3.geom.hull(hulls[i]) });
      }

      return hullset;
    }

    function drawCluster(d) {
      return curve(d.path); // 0.8
    }

    function deleteLink(data, update) {
      data.links.forEach(function (d, i) {
        if (d["label"] === update) {
          data.links.splice(i, 1);
        }
      });
    }

    function zoomed() {
      // vis.attr("transform", d3.event.transform);
      vis.attr(
        "transform", //svg下的g标签移动大小
        "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")"
      );
    }

    function dblclick(d) {
      d3.select(this).classed("fixed", (d.fixed = false));
    }

    function dragstart(d) {
      //这条语句可以解决：拖拽单个节点导致的整体移动问题
      d3.event.sourceEvent.stopPropagation();
      d3.select(this).classed("fixed", (d.fixed = true));
    }
    function init(nodeSize, linkSize) {
      if (force) force.stop();
      net = network(data, net, getGroup, collapse);

      force = d3.layout
        .force()
        .nodes(net.nodes)
        .links(net.links)
        .size([width, height])
        // eslint-disable-next-line no-unused-vars
        .linkDistance(function (l, i) {
          const n1 = l.source,
            n2 = l.target;
          // larger distance for bigger groups:
          // both between single nodes and _other_ groups (where size of own node group still counts),
          // and between two group nodes.
          //
          // reduce distance for groups with very few outer links,
          // again both in expanded and grouped form, i.e. between individual nodes of a group and
          // nodes of another group or other group node or between two group nodes.
          //
          // The latter was done to keep the single-link groups ('blue', rose, ...) close.
          return (
            30 +
            nodeSize / 2 +
            linkSize / 2 +
            Math.min(
              20 *
                Math.min(
                  n1.size || (n1.group !== n2.group ? n1.group_data.size : 1),
                  n2.size || (n1.group !== n2.group ? n2.group_data.size : 1)
                ),
              -30 +
                30 *
                  Math.min(
                    n1.link_count ||
                      (n1.group !== n2.group ? n1.group_data.link_count : 1),
                    n2.link_count ||
                      (n1.group !== n2.group ? n2.group_data.link_count : 1)
                  ),
              100
            )
          );
          //return 150;
        })
        // eslint-disable-next-line no-unused-vars
        .linkStrength(function (l, i) {
          return 1;
        })
        .gravity(0.01) // gravity+charge tweaked to ensure good 'grouped' view (e.g. green group not smack between blue&orange, ...
        .charge(-200) // 排斥/吸引，值越小越排斥... charge is important to turn single-linked groups to the outside
        .friction(0.4) // friction adjusted to get dampened display: less bouncy bouncy ball [Swedish Chef, anyone?]
        .start();

      var drag = force.drag().on("dragstart", dragstart);
      hullG.selectAll("path.hull").remove();
      hull = hullG
        .selectAll("path.hull")
        .data(convexHulls(net.nodes, getGroup, off))
        .enter()
        .append("path")
        .attr("class", "hull")
        .attr("d", drawCluster)
        .style("fill", "lightsteelblue")
        .style("fill-opacity", "0.3")
        .style("fill", function (d) {
          // console.log(d,fill(d.group));

          return fill(d.group);
        })
        // eslint-disable-next-line no-unused-vars
        .on("click", function (d) {
          // console.log("hull click", d, arguments, this, collapse[d.group]);
          // seletedData("hull click");
          // collapse[d.group] = true;
        });

      link = linkG.selectAll("line.link").data(net.links, linkId);
      link.exit().remove();
      link
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("x1", function (d) {
          return d.source.x;
        })
        .attr("y1", function (d) {
          return d.source.y;
        })
        .attr("x2", function (d) {
          return d.target.x;
        })
        .attr("y2", function (d) {
          return d.target.y;
        })
        .style("stroke", "#333")
        .style("stroke-opacity", "0.5")
        .style("stroke-width", function (d) {
          // console.log(d, "d.times:", d.size, "width-size:", linkscale(d.size));
          return linkScale(d.size);
          // return d.size || 2.5;
        })
        //连线右键菜单
        .on("contextmenu", function (d) {
          console.log("link right Click", d);
          deleteLink(data, d.id);
          d3.select(this).remove();
          d3.event.preventDefault();
          d3.event.stopPropagation();
        })
        .on("click", function (d) {
          console.log("link Click", d, this);
        });

      node = nodeG.selectAll("circle.node").data(net.nodes, nodeId);
      node.exit().remove();
      node
        .enter()
        .append("circle")
        // if (d.size) -- d.size > 0 when d is a group node.
        .attr("class", function (d) {
          return "node" + (d.size ? "" : " leaf");
        })
        //这里可以修改节点的大小
        // eslint-disable-next-line no-unused-vars
        .attr("r", function (d, i) {
          return nodeScale(d.times);
        })
        .attr("cx", function (d) {
          return d.x;
        })
        .attr("cy", function (d) {
          return d.y;
        })
        .style("fill", function (d) {
          // console.log(d,fill(d.group));
          return fill(d.group);
        })
        // eslint-disable-next-line no-unused-vars
        .on("click", function (d) {
          // console.log("node click", d, arguments, this, collapse[d.group]);
        });

      // node.call(force.drag);
      node.on("dblclick", dblclick).call(drag);

      svg.call(d3.behavior.zoom().scaleExtent([-1, 8]).on("zoom", zoomed));
      var nodeLabel = nodeG.selectAll("text.node").data(net.nodes, nodeId);
      nodeLabel.exit().remove();
      nodeLabel
        .enter()
        .append("text")
        .attr("class", "node")
        .attr("font-size", function (d) {
          // console.log("d.times:", d.times, "font-size:", fontscale(d.times));
          return fontScale(d.times);
        })
        .attr("text-anchor", "middle")
        // eslint-disable-next-line no-unused-vars
        .attr("fill", function (d) {
          // 这里应该是有bug的
          // return -fill(d.group);
        })
        .text(function (d) {
          return d.label;
        });
      force.on("tick", function () {
        if (!hull.empty()) {
          hull
            .data(convexHulls(net.nodes, getGroup, off))
            .attr("d", drawCluster);
        }

        link
          .attr("x1", function (d) {
            return d.source.x;
          })
          .attr("y1", function (d) {
            return d.source.y;
          })
          .attr("x2", function (d) {
            return d.target.x;
          })
          .attr("y2", function (d) {
            return d.target.y;
          });

        node
          .attr("cx", function (d) {
            return d.x;
          })
          .attr("cy", function (d) {
            return d.y;
          });
        nodeLabel
          .attr("x", function (d) {
            return d.x;
          })
          .attr("y", function (d) {
            return d.y;
          });
      });
    }

    d3.json(this.innerUrl, function (json) {
      data = json;
      /**************设置比例尺*************/
      //字体比例尺
      const nodeMaxTime = d3.max(data.nodes, function (d) {
        // console.log(typeof d.times);
        //     return parseInt(d.times);
        return parseFloat(d.times);
      });
      const nodeMinTime = d3.min(data.nodes, function (d) {
        return parseFloat(d.times);
      });
      const linkMaxTime = d3.max(data.links, function (d) {
        return parseFloat(d.times);
      });
      const linkMinTime = d3.min(data.links, function (d) {
        return parseFloat(d.times);
      });
      console.log(
        "nodemax:",
        nodeMaxTime,
        "nodemin:",
        nodeMinTime,
        "linkmax:",
        linkMaxTime,
        "linkmin:",
        linkMinTime
      );
      fontScale = d3.scale
        .linear()
        .domain([nodeMinTime, nodeMaxTime])
        .range([6, 18]);
      linkScale = d3.scale
        .linear()
        .domain([linkMinTime, linkMaxTime])
        .range([1, 5 + linkMaxTime / 3]);
      nodeScale = d3.scale
        .linear()
        .domain([nodeMinTime, nodeMaxTime])
        .range([8, 20 + nodeMaxTime / 2]);
      /**************设置比例尺结束***********/
      for (let i = 0; i < data.links.length; ++i) {
        let o = data.links[i];
        o.source = getNode(data.nodes, o.source);
        o.target = getNode(data.nodes, o.target);
        o.source = data.nodes[o.source];
        o.target = data.nodes[o.target];
      }
      hullG = vis.append("g");
      linkG = vis.append("g");
      nodeG = vis.append("g");
      init(nodeMaxTime, linkMaxTime);
      vis.attr("opacity", 1e-6).transition().duration(1000).attr("opacity", 1);
    });
  },

  methods: {},
};
</script>


<style scoped>
.graph-container {
  height: 100%;
  width: 100%;
}
#DrawGraph {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
</style>