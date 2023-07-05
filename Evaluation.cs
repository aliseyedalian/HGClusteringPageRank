namespace HGPRC
{
    public class Evaluation
    {
        public static Tuple<float, float, float, float> Confusion_matrix( 
            List<string> labels, 
            List<List<int>> results)
        {
            float tp = 0;
            float tn = 0;
            float fp = 0; 
            float fn = 0;
            for (int i = 0; i < labels.Count; i++)
            {
                for (int j = i+1; j < labels.Count; j++)
                {
                    bool have_commen_cluster = results[i].Intersect(results[j]).ToList().Count > 0;
                    if (labels[i] == labels[j] && have_commen_cluster) 
                    {
                        tp++;
                    }
                    else if (labels[i] != labels[j] && have_commen_cluster) 
                    {
                        fp++;
                    }
                    else if (labels[i] == labels[j] && !have_commen_cluster) 
                    {
                        fn++;
                    }
                    else if (labels[i] != labels[j] && !have_commen_cluster) 
                    {
                        tn++;
                    } 
                }
            }            
            return Tuple.Create(tp, fp, fn, tn);
        }
        public static float Precision(List<string> labels, List<List<int>> results)
        {
            Tuple<float, float, float, float> cm = Confusion_matrix(labels, results);
            float tp = cm.Item1;
            float fp = cm.Item2;  
            return tp/(tp+fp);
        }

        public static float RandIndex(List<string> labels, List<List<int>> results)
        {
           Tuple<float, float, float, float> cm = Confusion_matrix(labels, results);
           float tp = cm.Item1;
           float fp = cm.Item2;  
           float fn = cm.Item3;
           float tn = cm.Item4; 
           return (tp+tn)/(tp+tn+fn+fp);
        }
        public static float Recall(List<string> labels, List<List<int>> results)
        {
           Tuple<float, float, float, float> cm = Confusion_matrix(labels, results);
           float tp = cm.Item1;
           float fn = cm.Item3;
           return tp/(tp+fn);
        }
        public static float F_measure(List<string> labels, List<List<int>> results)
        {
           Tuple<float, float, float, float> cm = Confusion_matrix(labels, results);
           float tp = cm.Item1;
           float fp = cm.Item2;  
           float fn = cm.Item3;
           return 2*tp/(2*tp+fn+fp);
        }
        public static float Folkes_mallows(List<string> labels, List<List<int>> results)
        {
           Tuple<float, float, float, float> cm = Confusion_matrix(labels, results);
           float tp = cm.Item1;
           float fp = cm.Item2;  
           float fn = cm.Item3;
            return (float)(tp / Math.Sqrt((tp + fn) * (tp + fp)));
        }
    }
}