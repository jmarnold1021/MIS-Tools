USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_FA]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_FA]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_FA]
GO
/****** Object:  Table [dbo].[L56_DOD_FA]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_FA](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[GI03B] [varchar](3) NOT NULL,
	[SF21] [varchar](2) NOT NULL,
	[SF22] [int] NULL,
 CONSTRAINT [PK_DOD_FA_GI03_CCCCO_Assigned_GI03B_SF21] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC,
	[GI03B] ASC,
	[SF21] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO