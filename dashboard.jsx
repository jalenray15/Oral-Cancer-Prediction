import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, ScatterChart, Scatter, ZAxis, PieChart, Pie, Cell, ComposedChart } from 'recharts';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await window.fs.readFile('oral_cancer_processed.csv', { encoding: 'utf8' });
        
        // Parse CSV data
        import Papa from 'papaparse';
        const result = Papa.parse(response, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true
        });
        
        setData(result.data);
        setLoading(false);
      } catch (err) {
        console.error('Error loading data:', err);
        setError('Failed to load data. Please try again later.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Process data for various charts once data is loaded
  const processData = () => {
    if (!data) return null;

    // Process data for risk factor analysis
    const tobaccoData = processRiskFactorData('Tobacco Use');
    const alcoholData = processRiskFactorData('Alcohol Consumption');
    const combinedRiskData = processCombinedRiskData();
    const genderData = processGenderData();
    const treatmentData = processTreatmentData();
    const survivalByStageData = processSurvivalByStageData();
    const economicBurdenData = processEconomicBurdenData();
    const tumorSizeSurvivalData = processTumorSizeSurvivalData();
    
    return {
      tobaccoData,
      alcoholData,
      combinedRiskData,
      genderData,
      treatmentData,
      survivalByStageData,
      economicBurdenData,
      tumorSizeSurvivalData
    };
  };

  // Process data for risk factor analysis
  const processRiskFactorData = (riskFactor) => {
    const positiveCount = data.filter(item => item[riskFactor] === 'Yes' && item['Oral Cancer (Diagnosis)'] === 'Yes').length;
    const positiveTotal = data.filter(item => item[riskFactor] === 'Yes').length;
    const positiveRate = positiveTotal > 0 ? (positiveCount / positiveTotal) * 100 : 0;

    const negativeCount = data.filter(item => item[riskFactor] === 'No' && item['Oral Cancer (Diagnosis)'] === 'Yes').length;
    const negativeTotal = data.filter(item => item[riskFactor] === 'No').length;
    const negativeRate = negativeTotal > 0 ? (negativeCount / negativeTotal) * 100 : 0;

    return [
      { name: `${riskFactor}: Yes`, rate: positiveRate.toFixed(2), count: positiveCount, total: positiveTotal },
      { name: `${riskFactor}: No`, rate: negativeRate.toFixed(2), count: negativeCount, total: negativeTotal }
    ];
  };

  // Process data for combined risk factors
  const processCombinedRiskData = () => {
    const risksData = [];
    
    // Both tobacco and alcohol
    const bothCount = data.filter(item => 
      item['Tobacco Use'] === 'Yes' && 
      item['Alcohol Consumption'] === 'Yes' && 
      item['Oral Cancer (Diagnosis)'] === 'Yes'
    ).length;
    
    const bothTotal = data.filter(item => 
      item['Tobacco Use'] === 'Yes' && 
      item['Alcohol Consumption'] === 'Yes'
    ).length;
    
    const bothRate = bothTotal > 0 ? (bothCount / bothTotal) * 100 : 0;
    
    // Only tobacco
    const tobaccoOnlyCount = data.filter(item => 
      item['Tobacco Use'] === 'Yes' && 
      item['Alcohol Consumption'] === 'No' && 
      item['Oral Cancer (Diagnosis)'] === 'Yes'
    ).length;
    
    const tobaccoOnlyTotal = data.filter(item => 
      item['Tobacco Use'] === 'Yes' && 
      item['Alcohol Consumption'] === 'No'
    ).length;
    
    const tobaccoOnlyRate = tobaccoOnlyTotal > 0 ? (tobaccoOnlyCount / tobaccoOnlyTotal) * 100 : 0;
    
    // Only alcohol
    const alcoholOnlyCount = data.filter(item => 
      item['Tobacco Use'] === 'No' && 
      item['Alcohol Consumption'] === 'Yes' && 
      item['Oral Cancer (Diagnosis)'] === 'Yes'
    ).length;
    
    const alcoholOnlyTotal = data.filter(item => 
      item['Tobacco Use'] === 'No' && 
      item['Alcohol Consumption'] === 'Yes'
    ).length;
    
    const alcoholOnlyRate = alcoholOnlyTotal > 0 ? (alcoholOnlyCount / alcoholOnlyTotal) * 100 : 0;
    
    // Neither
    const neitherCount = data.filter(item => 
      item['Tobacco Use'] === 'No' && 
      item['Alcohol Consumption'] === 'No' && 
      item['Oral Cancer (Diagnosis)'] === 'Yes'
    ).length;
    
    const neitherTotal = data.filter(item => 
      item['Tobacco Use'] === 'No' && 
      item['Alcohol Consumption'] === 'No'
    ).length;
    
    const neitherRate = neitherTotal > 0 ? (neitherCount / neitherTotal) * 100 : 0;
    
    return [
      { name: 'Both', rate: bothRate.toFixed(2), count: bothCount, total: bothTotal },
      { name: 'Tobacco Only', rate: tobaccoOnlyRate.toFixed(2), count: tobaccoOnlyCount, total: tobaccoOnlyTotal },
      { name: 'Alcohol Only', rate: alcoholOnlyRate.toFixed(2), count: alcoholOnlyCount, total: alcoholOnlyTotal },
      { name: 'Neither', rate: neitherRate.toFixed(2), count: neitherCount, total: neitherTotal }
    ];
  };

  // Process data for gender analysis
  const processGenderData = () => {
    const maleCount = data.filter(item => item['Gender'] === 'Male' && item['Oral Cancer (Diagnosis)'] === 'Yes').length;
    const maleTotal = data.filter(item => item['Gender'] === 'Male').length;
    const maleRate = maleTotal > 0 ? (maleCount / maleTotal) * 100 : 0;

    const femaleCount = data.filter(item => item['Gender'] === 'Female' && item['Oral Cancer (Diagnosis)'] === 'Yes').length;
    const femaleTotal = data.filter(item => item['Gender'] === 'Female').length;
    const femaleRate = femaleTotal > 0 ? (femaleCount / femaleTotal) * 100 : 0;

    return [
      { name: 'Male', rate: maleRate.toFixed(2), count: maleCount, total: maleTotal },
      { name: 'Female', rate: femaleRate.toFixed(2), count: femaleCount, total: femaleTotal }
    ];
  };

  // Process data for treatment types
  const processTreatmentData = () => {
    const treatmentTypes = [...new Set(data.map(item => item['Treatment Type']))];
    
    return treatmentTypes.map(treatment => {
      const treatmentData = data.filter(item => item['Treatment Type'] === treatment);
      const avgSurvival = treatmentData.reduce((sum, item) => sum + item['Survival Rate (5-Year, %)'], 0) / treatmentData.length;
      
      return {
        name: treatment,
        avgSurvival: avgSurvival.toFixed(2)
      };
    });
  };

  // Process data for survival rates by cancer stage
  const processSurvivalByStageData = () => {
    const stages = [1, 2, 3, 4];
    
    return stages.map(stage => {
      const stageData = data.filter(item => item['Cancer Stage'] === stage);
      const avgSurvival = stageData.reduce((sum, item) => sum + item['Survival Rate (5-Year, %)'], 0) / stageData.length;
      
      return {
        name: `Stage ${stage}`,
        avgSurvival: avgSurvival.toFixed(2)
      };
    });
  };

  // Process data for economic burden
  const processEconomicBurdenData = () => {
    const stages = [1, 2, 3, 4];
    
    return stages.map(stage => {
      const stageData = data.filter(item => item['Cancer Stage'] === stage);
      const avgCost = stageData.reduce((sum, item) => sum + item['Cost of Treatment (USD)'], 0) / stageData.length;
      const avgBurden = stageData.reduce((sum, item) => sum + item['Economic Burden (Lost Workdays per Year)'], 0) / stageData.length;
      
      return {
        name: `Stage ${stage}`,
        avgCost: avgCost.toFixed(2),
        avgBurden: avgBurden.toFixed(2)
      };
    });
  };

  // Process data for tumor size vs survival rate
  const processTumorSizeSurvivalData = () => {
    // Take a sample of data points for better visualization
    const sampleSize = 500;
    const sampleStep = Math.floor(data.length / sampleSize);
    
    return data.filter((_, index) => index % sampleStep === 0)
      .map(item => ({
        tumorSize: item['Tumor Size (cm)'],
        survivalRate: item['Survival Rate (5-Year, %)'],
        stage: `Stage ${item['Cancer Stage']}`
      }));
  };

  // Tabs configuration
  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'riskFactors', label: 'Risk Factors' },
    { id: 'treatment', label: 'Treatment & Survival' },
    { id: 'economic', label: 'Economic Impact' }
  ];

  // Calculate dataset summary
  const getDataSummary = () => {
    if (!data) return null;
    
    const totalRecords = data.length;
    const positiveCases = data.filter(item => item['Oral Cancer (Diagnosis)'] === 'Yes').length;
    const negativeCases = data.filter(item => item['Oral Cancer (Diagnosis)'] === 'No').length;
    const positivePercentage = ((positiveCases / totalRecords) * 100).toFixed(1);
    const negativePercentage = ((negativeCases / totalRecords) * 100).toFixed(1);
    
    const averageAge = data.reduce((sum, item) => sum + item['Age'], 0) / totalRecords;
    const averageTumorSize = data.filter(item => item['Tumor Size (cm)'] > 0)
      .reduce((sum, item) => sum + item['Tumor Size (cm)'], 0) / 
      data.filter(item => item['Tumor Size (cm)'] > 0).length;
    
    const averageSurvival = data.reduce((sum, item) => sum + item['Survival Rate (5-Year, %)'], 0) / totalRecords;
    
    return {
      totalRecords,
      positiveCases,
      negativeCases,
      positivePercentage,
      negativePercentage,
      averageAge: averageAge.toFixed(1),
      averageTumorSize: averageTumorSize.toFixed(2),
      averageSurvival: averageSurvival.toFixed(1)
    };
  };

  // Charts and content by tab
  const renderTabContent = () => {
    const processedData = processData();
    if (!processedData) return <div>Processing data...</div>;
    
    switch (activeTab) {
      case 'overview':
        const summary = getDataSummary();
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-gray-500 text-sm font-medium">Total Records</h3>
                <p className="text-2xl font-bold">{summary.totalRecords.toLocaleString()}</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-gray-500 text-sm font-medium">Positive Cases</h3>
                <p className="text-2xl font-bold text-red-600">{summary.positiveCases.toLocaleString()} ({summary.positivePercentage}%)</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-gray-500 text-sm font-medium">Average Age</h3>
                <p className="text-2xl font-bold">{summary.averageAge} years</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-gray-500 text-sm font-medium">Average 5-Year Survival</h3>
                <p className="text-2xl font-bold">{summary.averageSurvival}%</p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Diagnosis Distribution</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'Positive', value: summary.positiveCases },
                          { name: 'Negative', value: summary.negativeCases }
                        ]}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                      >
                        <Cell fill="#FF8042" />
                        <Cell fill="#0088FE" />
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Survival Rate by Cancer Stage</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={processedData.survivalByStageData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis label={{ value: 'Avg. 5-Year Survival (%)', angle: -90, position: 'insideLeft' }} />
                      <Tooltip />
                      <Bar dataKey="avgSurvival" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Key Findings</h3>
              <ul className="list-disc pl-6 space-y-2">
                <li>Multiple risk factors have a compounding effect on oral cancer risk.</li>
                <li>Tumor size shows a strong negative correlation with 5-year survival rates.</li>
                <li>Early diagnosis significantly improves survival outcomes and reduces treatment costs.</li>
                <li>Treatment effectiveness varies by cancer stage, suggesting the need for stage-specific protocols.</li>
                <li>Both direct treatment costs and economic burden increase significantly with advanced cancer stages.</li>
              </ul>
            </div>
          </div>
        );
        
      case 'riskFactors':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Tobacco Use Impact</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={processedData.tobaccoData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis label={{ value: 'Cancer Diagnosis Rate (%)', angle: -90, position: 'insideLeft' }} />
                      <Tooltip />
                      <Bar dataKey="rate" fill="#FF8042" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Alcohol Consumption Impact</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={processedData.alcoholData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis label={{ value: 'Cancer Diagnosis Rate (%)', angle: -90, position: 'insideLeft' }} />
                      <Tooltip />
                      <Bar dataKey="rate" fill="#00C49F" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Combined Risk Factors Impact</h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={processedData.combinedRiskData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis label={{ value: 'Cancer Diagnosis Rate (%)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Bar dataKey="rate" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 text-sm text-gray-600">
                <p>This chart shows how the combination of risk factors significantly increases cancer diagnosis rates. Patients with both tobacco and alcohol use have substantially higher rates than those with a single risk factor or none.</p>
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Gender Distribution of Diagnosis Rates</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={processedData.genderData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis label={{ value: 'Cancer Diagnosis Rate (%)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Bar dataKey="rate" fill="#0088FE" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        );
        
      case 'treatment':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Treatment Effectiveness</h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={processedData.treatmentData} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" label={{ value: 'Avg. 5-Year Survival (%)', position: 'insideBottom', offset: -5 }} />
                      <YAxis type="category" dataKey="name" width={120} />
                      <Tooltip />
                      <Bar dataKey="avgSurvival" fill="#00C49F" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  <p>This chart compares average 5-year survival rates across different treatment types.</p>
                </div>
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-4">Tumor Size vs. Survival Rate</h3>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart
                      margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                    >
                      <CartesianGrid />
                      <XAxis 
                        type="number" 
                        dataKey="tumorSize" 
                        name="Tumor Size" 
                        unit="cm"
                        label={{ value: 'Tumor Size (cm)', position: 'insideBottom', offset: -5 }} 
                      />
                      <YAxis 
                        type="number" 
                        dataKey="survivalRate" 
                        name="Survival Rate" 
                        unit="%" 
                        label={{ value: '5-Year Survival Rate (%)', angle: -90, position: 'insideLeft' }}
                      />
                      <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                      <Scatter name="Tumor Size vs. Survival" data={processedData.tumorSizeSurvivalData} fill="#8884d8" />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  <p>This scatter plot shows the strong negative correlation between tumor size and 5-year survival rate.</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Key Treatment and Survival Insights</h3>
              <ul className="list-disc pl-6 space-y-2">
                <li>Tumor size is a powerful predictor of survival outcomes.</li>
                <li>Early diagnosis allows for less invasive treatments with higher success rates.</li>
                <li>Treatment efficacy varies significantly based on cancer stage.</li>
                <li>Combination therapies show better outcomes for advanced cases.</li>
                <li>Even with similar treatments, survival rates decrease as cancer stages advance.</li>
              </ul>
            </div>
          </div>
        );
        
      case 'economic':
        return (
          <div className="space-y-6">
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Economic Impact by Cancer Stage</h3>
              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={processedData.economicBurdenData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis yAxisId="left" label={{ value: 'Avg. Treatment Cost (USD)', angle: -90, position: 'insideLeft' }} />
                    <YAxis yAxisId="right" orientation="right" label={{ value: 'Lost Workdays per Year', angle: 90, position: 'insideRight' }} />
                    <Tooltip />
                    <Legend />
                    <Bar yAxisId="left" dataKey="avgCost" fill="#8884d8" name="Avg. Treatment Cost (USD)" />
                    <Line yAxisId="right" type="monotone" dataKey="avgBurden" stroke="#FF8042" name="Lost Workdays" />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 text-sm text-gray-600">
                <p>This chart illustrates how both treatment costs and economic burden (measured in lost workdays) increase significantly with advancing cancer stages. Early detection not only improves survival outcomes but also substantially reduces financial impact.</p>
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Economic Implications</h3>
              <ul className="list-disc pl-6 space-y-2">
                <li>Late-stage diagnosis dramatically increases treatment costs compared to early-stage treatment.</li>
                <li>Productivity losses (measured in lost workdays) follow a similar pattern, increasing substantially with advanced stages.</li>
                <li>Early detection programs demonstrate clear economic benefits through reduced treatment costs and productivity losses.</li>
                <li>Prevention strategies targeting high-risk populations could yield significant economic returns.</li>
                <li>The combined financial and productivity burden emphasizes the importance of early intervention and risk factor modification.</li>
              </ul>
            </div>
          </div>
        );
        
      default:
        return <div>Select a tab to view data</div>;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-lg">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center text-red-600">
          <p className="text-xl font-bold">Error</p>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 min-h-screen p-4">
      <div className="max-w-7xl mx-auto">
        <header className="bg-white p-6 rounded-lg shadow mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Oral Cancer Risk Factors and Outcomes Dashboard</h1>
          <p className="text-gray-600 mt-1">Analysis of 84,922 patient records examining risk factors, treatment outcomes, and economic impact</p>
        </header>
        
        <div className="bg-white rounded-lg shadow mb-6 overflow-hidden">
          <div className="flex border-b">
            {tabs.map(tab => (
              <button
                key={tab.id}
                className={`px-4 py-3 text-sm font-medium ${activeTab === tab.id ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>
          
          <div className="p-6">
            {renderTabContent()}
          </div>
        </div>
        
        <footer className="bg-white p-4 rounded-lg shadow text-center text-gray-600 text-sm">
          <p>Based on analysis of the Oral Cancer Prediction Dataset with 84,922 patient records</p>
        </footer>
      </div>
    </div>
  );
};

export default Dashboard;