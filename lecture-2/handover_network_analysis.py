"""
Social Network Analysis for Business Process Handover
Phân tích mạng xã hội cho quy trình giao việc nghiệp vụ
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import defaultdict
import seaborn as sns

# Set up Vietnamese font support
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (15, 10)

class HandoverNetworkAnalyzer:
    """
    Phân tích mạng lưới giao việc trong quy trình nghiệp vụ
    """
    
    def __init__(self, excel_file=None):
        self.G = nx.DiGraph()  # Directed graph for handover
        self.event_logs = []
        self.excel_file = excel_file
        
    def load_event_logs_from_excel(self, excel_file=None):
        """
        Đọc event logs từ file Excel
        
        Parameters:
        -----------
        excel_file : str
            Đường dẫn đến file Excel chứa event logs
            File phải có các cột: case_id, activity, timestamp, resource
        
        Returns:
        --------
        pd.DataFrame
            DataFrame chứa event logs
        """
        if excel_file is None:
            excel_file = self.excel_file
            
        if excel_file is None:
            raise ValueError("Vui lòng cung cấp đường dẫn đến file Excel")
        
        print(f"\n📂 Đang đọc event logs từ: {excel_file}")
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_file, sheet_name='Event Logs')
            
            # Validate required columns
            required_columns = ['case_id', 'activity', 'timestamp', 'resource']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"File Excel thiếu các cột: {missing_columns}")
            
            # Convert to list of dicts
            self.event_logs = df.to_dict('records')
            
            print(f"✅ Đọc thành công {len(df)} events từ file Excel")
            print(f"   📦 Số cases: {df['case_id'].nunique()}")
            print(f"   👥 Số resources: {df['resource'].nunique()}")
            print(f"   📋 Số activities: {df['activity'].nunique()}")
            
            return df
            
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file: {excel_file}")
            raise
        except Exception as e:
            print(f"❌ Lỗi khi đọc file Excel: {str(e)}")
            raise
    
    def build_handover_graph(self, df):
        """
        Xây dựng đồ thị handover từ event logs
        Handover: khi công việc chuyển từ người này sang người khác
        """
        # Group by case_id and sort by timestamp
        handovers = defaultdict(int)
        
        for case_id in df['case_id'].unique():
            case_events = df[df['case_id'] == case_id].sort_values('timestamp')
            resources = case_events['resource'].tolist()
            
            # Create edges for handovers (consecutive activities by different people)
            for i in range(len(resources) - 1):
                from_resource = resources[i]
                to_resource = resources[i + 1]
                
                if from_resource != to_resource:
                    handovers[(from_resource, to_resource)] += 1
        
        # Add edges to graph
        for (from_res, to_res), weight in handovers.items():
            self.G.add_edge(from_res, to_res, weight=weight)
        
        print(f"Đã tạo đồ thị với {self.G.number_of_nodes()} nodes và {self.G.number_of_edges()} edges")
        return self.G
    
    def calculate_degree_centrality(self):
        """
        1. DEGREE CENTRALITY (Độ trung tâm bậc)
        Đo lường: Số lượng kết nối trực tiếp
        Ý nghĩa: Người có nhiều kết nối = tham gia nhiều handover = quan trọng trong luồng công việc
        """
        print("\n" + "="*80)
        print("1. DEGREE CENTRALITY - Độ trung tâm bậc")
        print("="*80)
        
        # In-degree: Số lần nhận việc từ người khác
        in_degree = dict(self.G.in_degree())
        
        # Out-degree: Số lần giao việc cho người khác
        out_degree = dict(self.G.out_degree())
        
        # Total degree: Tổng số kết nối
        total_degree = {node: in_degree[node] + out_degree[node] for node in self.G.nodes()}
        
        # Normalized degree centrality (chuẩn hóa từ 0-1)
        degree_centrality = nx.degree_centrality(self.G.to_undirected())
        
        results = []
        for node in self.G.nodes():
            results.append({
                'Người tham gia': node,
                'In-Degree (Nhận việc)': in_degree[node],
                'Out-Degree (Giao việc)': out_degree[node],
                'Total Degree': total_degree[node],
                'Degree Centrality': round(degree_centrality[node], 4)
            })
        
        df_degree = pd.DataFrame(results).sort_values('Total Degree', ascending=False)
        print("\n", df_degree.to_string(index=False))
        
        most_connected = df_degree.iloc[0]['Người tham gia']
        print(f"\n👤 Người có nhiều kết nối nhất: {most_connected}")
        print(f"   → Tham gia nhiều handover, là hub trong quy trình")
        
        return df_degree
    
    def calculate_betweenness_centrality(self):
        """
        2. BETWEENNESS CENTRALITY (Độ trung tâm trung gian)
        Đo lường: Số lần một người nằm trên đường đi ngắn nhất giữa các người khác
        Ý nghĩa: "Người gác cổng" - kiểm soát luồng thông tin/công việc giữa các nhóm
        """
        print("\n" + "="*80)
        print("2. BETWEENNESS CENTRALITY - Độ trung tâm trung gian (Gatekeeper)")
        print("="*80)
        
        betweenness = nx.betweenness_centrality(self.G, normalized=True)
        
        results = []
        for node, score in betweenness.items():
            results.append({
                'Người tham gia': node,
                'Betweenness Centrality': round(score, 4),
                'Vai trò': 'Gatekeeper cao' if score > 0.1 else 'Gatekeeper thấp'
            })
        
        df_betweenness = pd.DataFrame(results).sort_values('Betweenness Centrality', ascending=False)
        print("\n", df_betweenness.to_string(index=False))
        
        gatekeeper = df_betweenness.iloc[0]['Người tham gia']
        print(f"\n🚪 Người gác cổng chính (Gatekeeper): {gatekeeper}")
        print(f"   → Kiểm soát luồng công việc giữa các phòng ban/nhóm")
        print(f"   → Nếu người này nghỉ việc, quy trình có thể bị gián đoạn")
        
        return df_betweenness
    
    def calculate_closeness_centrality(self):
        """
        3. CLOSENESS CENTRALITY (Độ trung tâm gần gũi)
        Đo lường: Mức độ gần gũi với tất cả các nút khác
        Ý nghĩa: Người có khả năng tiếp cận nhanh với tất cả mọi người trong mạng
        """
        print("\n" + "="*80)
        print("3. CLOSENESS CENTRALITY - Độ trung tâm gần gũi (Nhanh nhạy)")
        print("="*80)
        
        # For directed graph, we use in/out closeness
        try:
            closeness_in = nx.closeness_centrality(self.G.reverse(), distance='weight')
            closeness_out = nx.closeness_centrality(self.G, distance='weight')
        except:
            # If graph is not strongly connected, use undirected
            G_undirected = self.G.to_undirected()
            closeness = nx.closeness_centrality(G_undirected)
            closeness_in = closeness
            closeness_out = closeness
        
        results = []
        for node in self.G.nodes():
            avg_closeness = (closeness_in[node] + closeness_out[node]) / 2
            results.append({
                'Người tham gia': node,
                'Closeness In': round(closeness_in[node], 4),
                'Closeness Out': round(closeness_out[node], 4),
                'Avg Closeness': round(avg_closeness, 4)
            })
        
        df_closeness = pd.DataFrame(results).sort_values('Avg Closeness', ascending=False)
        print("\n", df_closeness.to_string(index=False))
        
        most_close = df_closeness.iloc[0]['Người tham gia']
        print(f"\n⚡ Người nhanh nhạy nhất: {most_close}")
        print(f"   → Có khả năng tiếp cận nhanh với mọi người trong mạng")
        print(f"   → Phù hợp làm người điều phối hoặc truyền đạt thông tin khẩn cấp")
        
        return df_closeness
    
    def calculate_eigenvector_centrality(self):
        """
        4. EIGENVECTOR CENTRALITY (Độ trung tâm vector riêng)
        Đo lường: Uy tín dựa trên chất lượng kết nối
        Ý nghĩa: Không chỉ đếm số kết nối, mà còn xem người kết nối có "uy tín" không
        """
        print("\n" + "="*80)
        print("4. EIGENVECTOR CENTRALITY - Độ trung tâm uy tín")
        print("="*80)
        
        try:
            # For directed graph
            eigenvector = nx.eigenvector_centrality(self.G, max_iter=1000)
        except:
            # If doesn't converge, use undirected
            G_undirected = self.G.to_undirected()
            eigenvector = nx.eigenvector_centrality(G_undirected, max_iter=1000)
        
        results = []
        for node, score in eigenvector.items():
            results.append({
                'Người tham gia': node,
                'Eigenvector Centrality': round(score, 4),
                'Mức uy tín': 'Rất cao' if score > 0.3 else ('Cao' if score > 0.2 else 'Trung bình')
            })
        
        df_eigenvector = pd.DataFrame(results).sort_values('Eigenvector Centrality', ascending=False)
        print("\n", df_eigenvector.to_string(index=False))
        
        most_prestigious = df_eigenvector.iloc[0]['Người tham gia']
        print(f"\n⭐ Người có uy tín cao nhất: {most_prestigious}")
        print(f"   → Kết nối với những người quan trọng trong mạng")
        print(f"   → Có ảnh hưởng lớn trong tổ chức")
        
        return df_eigenvector
    
    def identify_key_person(self, df_degree, df_betweenness, df_closeness, df_eigenvector):
        """
        Xác định người quan trọng nhất dựa trên tổng hợp các chỉ số
        """
        print("\n" + "="*80)
        print("TỔNG HỢP: XÁC ĐỊNH NGƯỜI QUAN TRỌNG NHẤT TRONG HỆ THỐNG")
        print("="*80)
        
        # Normalize scores to 0-1 scale
        all_people = list(self.G.nodes())
        scores = {}
        
        for person in all_people:
            degree_score = df_degree[df_degree['Người tham gia'] == person]['Degree Centrality'].values[0]
            betweenness_score = df_betweenness[df_betweenness['Người tham gia'] == person]['Betweenness Centrality'].values[0]
            closeness_score = df_closeness[df_closeness['Người tham gia'] == person]['Avg Closeness'].values[0]
            eigenvector_score = df_eigenvector[df_eigenvector['Người tham gia'] == person]['Eigenvector Centrality'].values[0]
            
            # Weighted average (có thể điều chỉnh trọng số)
            total_score = (
                degree_score * 0.25 +
                betweenness_score * 0.35 +  # Gatekeeper quan trọng nhất
                closeness_score * 0.20 +
                eigenvector_score * 0.20
            )
            
            scores[person] = {
                'Degree': round(degree_score, 3),
                'Betweenness': round(betweenness_score, 3),
                'Closeness': round(closeness_score, 3),
                'Eigenvector': round(eigenvector_score, 3),
                'Tổng điểm': round(total_score, 3)
            }
        
        # Create summary dataframe
        df_summary = pd.DataFrame(scores).T.reset_index()
        df_summary.columns = ['Người tham gia', 'Degree', 'Betweenness', 'Closeness', 'Eigenvector', 'Tổng điểm']
        df_summary = df_summary.sort_values('Tổng điểm', ascending=False)
        
        print("\n", df_summary.to_string(index=False))
        
        # Identify the most important person
        key_person = df_summary.iloc[0]['Người tham gia']
        key_score = df_summary.iloc[0]['Tổng điểm']
        
        print(f"\n{'🏆'*40}")
        print(f"🏆 NGƯỜI QUAN TRỌNG NHẤT: {key_person}")
        print(f"🏆 Điểm tổng hợp: {key_score}")
        print(f"{'🏆'*40}")
        
        print("\n📊 Phân tích vai trò:")
        for idx, row in df_summary.head(3).iterrows():
            person = row['Người tham gia']
            print(f"\n{idx+1}. {person}:")
            if row['Betweenness'] > 0.15:
                print(f"   ✓ Gatekeeper - Kiểm soát luồng công việc")
            if row['Degree'] > 0.3:
                print(f"   ✓ Hub - Trung tâm kết nối")
            if row['Closeness'] > 0.4:
                print(f"   ✓ Coordinator - Điều phối hiệu quả")
            if row['Eigenvector'] > 0.3:
                print(f"   ✓ Influencer - Có ảnh hưởng cao")
        
        return df_summary
    
    def visualize_network(self, df_summary):
        """
        Vẽ đồ thị mạng lưới handover với visualization chuyên nghiệp
        """
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('SOCIAL NETWORK ANALYSIS - Business Process Handover Graph', 
                     fontsize=20, fontweight='bold', y=0.995)
        
        # Position layout
        pos = nx.spring_layout(self.G, k=2, iterations=50, seed=42)
        
        # Get node sizes based on total score
        node_sizes = []
        node_colors = []
        for node in self.G.nodes():
            score = df_summary[df_summary['Người tham gia'] == node]['Tổng điểm'].values[0]
            node_sizes.append(score * 5000 + 500)
            node_colors.append(score)
        
        # Get edge weights
        edge_weights = [self.G[u][v]['weight'] for u, v in self.G.edges()]
        max_weight = max(edge_weights) if edge_weights else 1
        edge_widths = [w / max_weight * 5 for w in edge_weights]
        
        # 1. Main Network Graph with all centrality
        ax1 = axes[0, 0]
        nx.draw_networkx_nodes(self.G, pos, node_size=node_sizes, 
                              node_color=node_colors, cmap='YlOrRd',
                              alpha=0.9, ax=ax1)
        nx.draw_networkx_labels(self.G, pos, font_size=10, 
                               font_weight='bold', ax=ax1)
        nx.draw_networkx_edges(self.G, pos, width=edge_widths, 
                              alpha=0.6, edge_color='gray',
                              arrows=True, arrowsize=20, 
                              arrowstyle='->', ax=ax1,
                              connectionstyle='arc3,rad=0.1')
        ax1.set_title('Handover Network (Node size = Importance)', 
                     fontsize=14, fontweight='bold')
        ax1.axis('off')
        
        # 2. Degree Centrality
        ax2 = axes[0, 1]
        degree_dict = nx.degree_centrality(self.G.to_undirected())
        degree_sizes = [degree_dict[node] * 5000 + 500 for node in self.G.nodes()]
        degree_colors = [degree_dict[node] for node in self.G.nodes()]
        
        nx.draw_networkx_nodes(self.G, pos, node_size=degree_sizes,
                              node_color=degree_colors, cmap='Blues',
                              alpha=0.9, ax=ax2)
        nx.draw_networkx_labels(self.G, pos, font_size=10,
                               font_weight='bold', ax=ax2)
        nx.draw_networkx_edges(self.G, pos, width=edge_widths,
                              alpha=0.4, edge_color='gray',
                              arrows=True, arrowsize=15,
                              arrowstyle='->', ax=ax2,
                              connectionstyle='arc3,rad=0.1')
        ax2.set_title('Degree Centrality (Kết nối nhiều)', 
                     fontsize=14, fontweight='bold')
        ax2.axis('off')
        
        # 3. Betweenness Centrality
        ax3 = axes[1, 0]
        betweenness_dict = nx.betweenness_centrality(self.G)
        betweenness_sizes = [betweenness_dict[node] * 8000 + 500 for node in self.G.nodes()]
        betweenness_colors = [betweenness_dict[node] for node in self.G.nodes()]
        
        nx.draw_networkx_nodes(self.G, pos, node_size=betweenness_sizes,
                              node_color=betweenness_colors, cmap='Greens',
                              alpha=0.9, ax=ax3)
        nx.draw_networkx_labels(self.G, pos, font_size=10,
                               font_weight='bold', ax=ax3)
        nx.draw_networkx_edges(self.G, pos, width=edge_widths,
                              alpha=0.4, edge_color='gray',
                              arrows=True, arrowsize=15,
                              arrowstyle='->', ax=ax3,
                              connectionstyle='arc3,rad=0.1')
        ax3.set_title('Betweenness Centrality (Gatekeeper)', 
                     fontsize=14, fontweight='bold')
        ax3.axis('off')
        
        # 4. Summary Bar Chart
        ax4 = axes[1, 1]
        top_5 = df_summary.head(5)
        colors_bar = plt.cm.RdYlGn(np.linspace(0.4, 0.9, len(top_5)))
        
        bars = ax4.barh(top_5['Người tham gia'], top_5['Tổng điểm'], 
                       color=colors_bar, alpha=0.8, edgecolor='black')
        ax4.set_xlabel('Tổng điểm Centrality', fontsize=12, fontweight='bold')
        ax4.set_title('Top 5 Người Quan Trọng Nhất', 
                     fontsize=14, fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, top_5['Tổng điểm'])):
            ax4.text(value + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{value:.3f}', va='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Save figure
        output_path = '/mnt/user-data/outputs/handover_network_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n📊 Đồ thị đã được lưu tại: {output_path}")
        
        return output_path
    
    def create_detailed_report(self, df_summary):
        """
        Tạo báo cáo chi tiết dưới dạng CSV
        """
        # Event logs
        df_events = pd.DataFrame(self.event_logs)
        
        # Handover matrix
        handover_matrix = []
        edges_data = [(u, v, self.G[u][v]['weight']) for u, v in self.G.edges()]
        for from_res, to_res, weight in sorted(edges_data, key=lambda x: x[2], reverse=True):
            handover_matrix.append({
                'From': from_res,
                'To': to_res,
                'Handover Count': weight
            })
        df_handovers = pd.DataFrame(handover_matrix)
        
        # Save to Excel
        output_excel = '/mnt/user-data/outputs/handover_analysis_report.xlsx'
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            df_events.to_excel(writer, sheet_name='Event Logs', index=False)
            df_handovers.to_excel(writer, sheet_name='Handover Matrix', index=False)
            df_summary.to_excel(writer, sheet_name='Centrality Summary', index=False)
        
        print(f"\n📄 Báo cáo Excel đã được lưu tại: {output_excel}")
        return output_excel


def main(excel_file=None):
    """
    Main function to run the analysis
    
    Parameters:
    -----------
    excel_file : str, optional
        Đường dẫn đến file Excel chứa event logs
        Nếu không cung cấp, sẽ tìm file event_logs.xlsx trong thư mục outputs
    """
    print("="*80)
    print("SOCIAL NETWORK ANALYSIS FOR BUSINESS PROCESS HANDOVER")
    print("Phân tích mạng xã hội cho quy trình giao việc nghiệp vụ")
    print("="*80)
    
    # Default Excel file path
    if excel_file is None:
        excel_file = '/mnt/user-data/outputs/event_logs.xlsx'
    
    # Initialize analyzer
    analyzer = HandoverNetworkAnalyzer(excel_file=excel_file)
    
    # Load event logs from Excel
    print("\n📋 Bước 1: Đọc dữ liệu Event Logs từ Excel")
    try:
        df_events = analyzer.load_event_logs_from_excel()
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        print("\n💡 Hướng dẫn:")
        print("   1. Chuẩn bị file Excel với sheet 'Event Logs'")
        print("   2. File phải có 4 cột: case_id, activity, timestamp, resource")
        print("   3. Chạy lại với: main('đường_dẫn_file.xlsx')")
        return
    
    # Build handover graph
    print("\n🔗 Bước 2: Xây dựng đồ thị Handover")
    analyzer.build_handover_graph(df_events)
    
    # Calculate centrality metrics
    print("\n📊 Bước 3: Tính toán các độ đo Centrality")
    df_degree = analyzer.calculate_degree_centrality()
    df_betweenness = analyzer.calculate_betweenness_centrality()
    df_closeness = analyzer.calculate_closeness_centrality()
    df_eigenvector = analyzer.calculate_eigenvector_centrality()
    
    # Identify key person
    print("\n🎯 Bước 4: Xác định người quan trọng nhất")
    df_summary = analyzer.identify_key_person(
        df_degree, df_betweenness, df_closeness, df_eigenvector
    )
    
    # Visualize
    print("\n🎨 Bước 5: Vẽ đồ thị visualization")
    analyzer.visualize_network(df_summary)
    
    # Create report
    print("\n📝 Bước 6: Tạo báo cáo chi tiết")
    analyzer.create_detailed_report(df_summary)
    
    print("\n" + "="*80)
    print("✅ HOÀN THÀNH PHÂN TÍCH!")
    print("="*80)
    print("\n📂 Các file kết quả:")
    print("   - handover_network_analysis.png (Visualization)")
    print("   - handover_analysis_report.xlsx (Báo cáo chi tiết)")
    print("   - handover_network_interactive.html (Website tương tác)")


if __name__ == "__main__":
    import sys
    
    # Allow command line argument for Excel file
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
        main(excel_file)
    else:
        # Use default file
        main()
