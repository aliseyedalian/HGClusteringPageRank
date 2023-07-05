using System.Diagnostics;
using MathNet.Numerics.LinearAlgebra;
using Newtonsoft.Json;
using static HGPRC.Evaluation;


namespace HGPRC
{
    class MainClass
    {
        public static List<string> Local_clustering(Hypergraph HG, int v_init, double mu)
        {
            var time = new Stopwatch();
            time.Start();

            int n = HG.n;
            int m = HG.m;

            const double eps = 0.9;
            
            const double dt = 1.0;
            const double T = 30.0;

            var A_cand = new List<double>();
            for (int i = 0; i <= Math.Log(n * m) / Math.Log(1 + eps); i++)
            {
                A_cand.Add(Math.Pow(1 + eps, i) / (n * m));
            }

            var edge_size = new Dictionary<int, int>();
            for (int eid = 0; eid < HG.m; eid++)
            {
                edge_size.Add(eid, HG.ID_rev[eid].Count);
            }

            double min_conductance = double.MaxValue;
            List<int> best_vertex_set = new();


            foreach (double alpha in A_cand)
            {

                var vec = CreateVector.Dense<double>(n);

                vec[v_init] = 1.0;

                vec = Hypergraph.Simulate_round(HG, vec, v_init, dt, T, alpha);
                // vec = Hypergraph.Simulate(HG, vec, v_init, dt, T, alpha);

                for (int i = 0; i < n; i++)
                {
                    vec[i] /= HG.W_Degree(i);
                }

                int[] index = Enumerable.Range(0, n).ToArray();
                Array.Sort(index, (a, b) => vec[a].CompareTo(vec[b]));

                Array.Reverse(index);

                double vol_V = 0;
                for (int i = 0; i < n; i++) vol_V += HG.W_Degree(i);

                var num_contained_nodes = new Dictionary<int, int>();
                for (int eid = 0; eid < HG.m; eid++)
                {
                    num_contained_nodes.Add(eid, 0);
                }

                double cut_val = 0;
                double vol_S = 0;
                double conductance = double.MaxValue;
                List<int> vertex_set = new();


                foreach (int i in index)
                {
                    vol_S += HG.W_Degree(i);
                    vertex_set.Add(i);

                    if (vol_S/vol_V <= mu)
                    {
                        foreach (var e in HG.incident_edges[i])
                        {
                            if (num_contained_nodes[e] == 0)
                            {
                                cut_val += HG.weights[e];
                            }
                            if (num_contained_nodes[e] == edge_size[e] - 1)
                            {
                                cut_val -= HG.weights[e];
                            }
                            num_contained_nodes[e] += 1;
                        }  
                        conductance = cut_val / Math.Min(vol_S, vol_V - vol_S);
                        if (conductance < min_conductance)
                        {
                            min_conductance = conductance;
                            best_vertex_set.Clear();
                            best_vertex_set.AddRange(vertex_set);
                        }
                    }
                    else
                    {
                        break;
                    }
                }
            }

            // // Replace each vertex i in the best_vertex_set with its corresponding name
            List<string> cluster = new();
            if (!best_vertex_set.Contains(v_init))
            {
                best_vertex_set.Add(v_init);
            }
            for (int i = 0; i < best_vertex_set.Count; i++)
            {
                cluster.Add(HG.node_name[best_vertex_set[i]]); 
            } 

            time.Stop();
            Console.WriteLine("time (s): " + time.ElapsedMilliseconds/1000.0);
            return cluster;
        }
        public static List<string> Extend_cluster (List<string> cluster,Hypergraph HG)
        {
            HashSet<string> extended_cluster = cluster.ToHashSet();
            HashSet<int> visited_edges = new();
            List<int> cluster_ids = new();
            List<int> edge = new();
            List<int> intersection = new();
            foreach (string name in cluster)
            {
                cluster_ids.Add(HG.node_id[name]);
            }
            foreach (string n in cluster)
            {
                foreach (int e in HG.incident_edges[HG.node_id[n]])
                {
                    edge = HG.edges[e];
                    intersection = cluster_ids.Intersect(edge).ToList(); 
                    if ((!visited_edges.Contains(e)) && (intersection.Count >= (float)edge.Count / 2))
                    {
                        foreach (int id in edge)
                        {
                            extended_cluster.Add(HG.node_name[id]);
                        }
                    }
                    visited_edges.Add(e); 
                }
            }
            return extended_cluster.ToList();
        }

        public static Dictionary<int, List<int>> Get_adjacency_dictionary(Hypergraph HG)
        {   // neighbors of each node.
            var adj_dict = new Dictionary<int, List<int>>();
            foreach (int node in HG.node_id.Values)
            {
                HashSet<int> neighbors = new();
                foreach (int e in HG.incident_edges[node])
                {
                    foreach (int n in HG.edges[e])
                    {
                        if (n != node)
                        {
                            neighbors.Add(n);
                        }
                    }
                }
                adj_dict[node] = neighbors.ToList();
            }
            return adj_dict;
        }
        public static List<int> W_Degree_nodes_priority(Hypergraph HG, bool Reverse)
        {
            // (v,HG.W_Degree(v)) dictionary and sort based on value
            Dictionary<int,double> W_Degree_dict = new();
            for (int v = 0; v < HG.n ; v++) 
            {
                W_Degree_dict[v] = HG.W_Degree(v);
            }
            if (Reverse)
            {
                W_Degree_dict = W_Degree_dict.OrderByDescending(x => x.Value).ToDictionary(x => x.Key, x => x.Value);
            }
            else
            {
                W_Degree_dict = W_Degree_dict.OrderBy(x => x.Value).ToDictionary(x => x.Key, x => x.Value);
            }
            List<int> result = W_Degree_dict.Keys.ToList();
            return result;
        }
        static List<int> Betweenness_nodes_priority(Hypergraph HG)
        {
            var script = @"pythonScripts/betweenness.py";
            Dictionary<int, List<int>> adjacency_dictionary = Get_adjacency_dictionary(HG);
            string json = JsonConvert.SerializeObject(adjacency_dictionary);
            ProcessStartInfo psi = new()
            {  
                FileName = @"/usr/bin/python3",
                Arguments = string.Format("{0} {1}", script, json),
                UseShellExecute = false,
                CreateNoWindow = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
            };
            var errors = "";
            var result = "";
            using (var process = Process.Start(psi))
            {
                if (process != null)
                {
                    errors = process.StandardError.ReadToEnd();
                    result = process.StandardOutput.ReadToEnd();
                }
            }
            List<int> output = new();
            output = result[1..^2].Split(',').Select(int.Parse).ToList();
            return output;
        }
        public static List<string> Get_labels(string file_lbl) 
        {
            List<string> labels = new();
            var fs = new FileStream(file_lbl, FileMode.Open);
            var sr = new StreamReader(fs);
            for (string? line; (line = sr.ReadLine()) != null;)
            {
                labels.Add(line);    
            }
            fs.Close();
            return labels;
        }
        public static List<List<int>> Get_results(List<List<string>> clusters, Hypergraph HG)
        {
            Dictionary<int,List<int>> nodeClustersDict = new();
            for (int cid = 0; cid < clusters.Count; cid++)
            {
                List<string> cluster = clusters[cid];
                foreach (string node in cluster)
                {
                    int nid = HG.node_id[node];
                    if (nodeClustersDict.ContainsKey(nid))
                    {
                        nodeClustersDict[nid].Add(cid);
                    }
                    else
                    {
                        nodeClustersDict[nid] = new List<int>();
                        nodeClustersDict[nid].Add(cid);
                    }
                }

            }
            nodeClustersDict = nodeClustersDict.OrderBy(x => x.Key).ToDictionary(kvp => kvp.Key, kvp => kvp.Value);;
            List<List<int>> results = nodeClustersDict.Values.ToList();
            return results;
        }
        public static List<List<string>> Pagerank_clustering_overlap(string file_in, 
        string file_out, 
        double mu, 
        string? file_lbl = default)
        {
            Hypergraph HG = Hypergraph.Open(file_in);
            Console.WriteLine("Pagerank clustering with overlap (HGPRCO):");
            var totalTime = new Stopwatch();
            totalTime.Start();
            List<int> nodes_priority = W_Degree_nodes_priority(HG,true);
            // List<string> nodes_priority_names = new();
            // foreach (var node in nodes_priority)
            // {
            //     nodes_priority_names.Add(HG.node_name[node]);
            // }
            // Console.WriteLine(string.Join(", ", nodes_priority_names));
            int node_init;
            List<string> new_cluster;
            List<List<string>> clusters = new();
            while (nodes_priority.Count != 0)
            {
                node_init = nodes_priority[0];
                nodes_priority.RemoveAt(0);
                Console.WriteLine("node init: "+HG.node_name[node_init]);
                new_cluster = Local_clustering(HG, node_init, mu);
                // new_cluster = Extend_cluster(new_cluster,HG);
                if (new_cluster.Count != 0)
                {
                    clusters.Add(new_cluster);
                    foreach (string node in new_cluster)
                    {
                        nodes_priority.Remove(HG.node_id[node]);
                    }
                }
                Console.WriteLine("remain nodes: " + nodes_priority.Count);
            }

            StreamWriter Writer = new(file_out);
            foreach (var cluster in clusters)  
            {
                Writer.WriteLine("["+string.Join(", ",cluster)+"]");
            }
            Writer.Close();
            if (file_lbl!=null)
            {
                Console.WriteLine("\n- Evaluation :");
                List<string> lbl = Get_labels(file_lbl);
                List<List<int>> res = Get_results(clusters, HG);
                Tuple<float, float, float, float> cm = Confusion_matrix(lbl, res);
                Console.WriteLine("tp, fp, fn, tn");
                Console.WriteLine(string.Join(",",cm));
                Console.WriteLine("Precision = "+Precision(lbl, res));
                Console.WriteLine("Recall = "+Recall(lbl, res));
                Console.WriteLine("RandIndex = "+RandIndex(lbl, res));
                Console.WriteLine("F_measure = "+F_measure(lbl, res));
                Console.WriteLine("Folkes_mallows = "+Folkes_mallows(lbl, res));
            }
            totalTime.Stop();
            Console.WriteLine("\n-> Total Time (s): " + totalTime.ElapsedMilliseconds/1000.0);
            return clusters;   
        }

        public static void Pause()
        {
            Console.Write("Press any key to continue... ");
            Console.ReadKey(true);
        }

        public static void Main(string[] args)
        {
            // string fn_in = "instance/Toy_samples/tiny_hg.txt";
            // string fn_out = "instance/Toy_samples/clusters_tiny_hg.txt";        
            string fn_in = "instance/sampleWithBenchmark/house-committees/hyperedges-house-committees_formate.txt";
            string fn_out = "instance/sampleWithBenchmark/house-committees/clusters_hyperedges-house-committees_formate.txt";    
            string fn_lbl = "instance/sampleWithBenchmark/house-committees/node-labels-house-committees.txt";
            double mu = 0.1;
            Pagerank_clustering_overlap(fn_in,fn_out,mu,fn_lbl); // HGPRCO

            Pause();
        }
    }
}