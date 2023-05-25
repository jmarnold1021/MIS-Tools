USE [ODS_production]
GO
/****** Object:  Table [dbo].[L56_DOD_SP]    Script Date: 5/12/2023 12:01:39 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SP]') AND type in (N'U'))
DROP TABLE [dbo].[L56_DOD_SP]
GO
/****** Object:  Table [dbo].[L56_DOD_SP]    Script Date: 5/12/2023 12:01:39 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[L56_DOD_SP](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[SP01] [varchar](6) NULL,
	[SP02] [varchar](1) NULL,
	[SP03] [varchar](8) NULL,
	[GI92] [varchar](1) NOT NULL,
	[SP04] [varchar](5) NOT NULL,
 CONSTRAINT [PK_DOD_SP_GI03_CCCCO_Assigned_GI92_SP04] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC,
	[GI92] ASC,
	[SP04] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
